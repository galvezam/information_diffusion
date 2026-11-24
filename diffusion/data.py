"""Read compressed SNAP files and choose a small graph without activity labels."""
from collections import deque
from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy import sparse

START = pd.Timestamp("2012-07-01", tz="UTC")
HOURS = 168


def load_activity(path):
    events = pd.read_csv(path, sep=r"\s+", names=["actor", "target", "timestamp", "kind"],
                         dtype={"actor": "int32", "target": "int32", "timestamp": "int64", "kind": "category"})
    events["hour"] = (events.timestamp - START.timestamp()) / 3600
    if not events.hour.between(0, HOURS, inclusive="left").all():
        raise ValueError("Expected the July 1–7, 2012 observation window.")
    return events


def reverse_social_edges(follow_edges):
    """Raw A -> B means A follows B. Information flows B -> A."""
    return follow_edges[:, ::-1]


def sample_social(path, n_nodes=5000, seed=42, cache_dir=".cache"):
    """Randomized breadth-first sample; induced edges retain their direction.

    The full graph is sparse, never a Python object per edge or a dense matrix.
    Sampling uses topology only, but favors connected/high-degree neighborhoods.
    """
    path = Path(path)
    signature = dict(path=str(path.resolve()), size=path.stat().st_size,
                     mtime=path.stat().st_mtime_ns, n_nodes=n_nodes, seed=seed, version=1)
    cache = Path(cache_dir) / f"social-{n_nodes}-{seed}"
    if cache.with_suffix(".json").exists():
        meta = json.loads(cache.with_suffix(".json").read_text())
        if meta["signature"] == signature:
            return (sparse.load_npz(cache.with_suffix(".npz")),
                    np.load(cache.with_suffix(".npy")), meta)
    if n_nodes < 2:
        raise ValueError("n_nodes must be at least 2")
    # About 120 MB for 15 million pairs of int32 IDs; one reader/process.
    edges = pd.read_csv(path, sep=r"\s+", header=None, dtype="int32").to_numpy()
    ids = np.unique(edges)
    if n_nodes > len(ids):
        raise ValueError(f"Only {len(ids)} nodes are available")
    flow = reverse_social_edges(edges)
    graph = sparse.csr_matrix((np.ones(len(flow), dtype=bool), (flow[:, 0], flow[:, 1])),
                              shape=(int(ids.max()) + 1,) * 2)
    full_edges = graph.nnz
    del edges, flow
    undirected = graph.maximum(graph.T)
    rng = np.random.default_rng(seed)
    root = int(rng.choice(ids))
    selected, seen, queue = [root], {root}, deque([root])
    while len(selected) < n_nodes:
        if not queue:
            # A disconnected component may be smaller than the requested sample.
            root = int(rng.choice(ids[~np.isin(ids, selected)]))
            selected.append(root)
            seen.add(root)
            queue.append(root)
        node = queue.popleft()
        neighbors = undirected.indices[undirected.indptr[node]:undirected.indptr[node + 1]]
        for neighbor in rng.permutation(neighbors):
            if len(selected) == n_nodes:
                break
            if int(neighbor) not in seen:
                seen.add(int(neighbor))
                selected.append(int(neighbor))
                queue.append(int(neighbor))
    selected = np.array(sorted(selected), dtype=np.int32)
    graph = graph[selected][:, selected].astype(np.float64)
    graph.setdiag(0)
    graph.eliminate_zeros()
    graph.data[:] = 1
    meta = dict(signature=signature, full_nodes=len(ids), full_edges=full_edges,
                sample_nodes=len(selected), sample_edges=graph.nnz,
                sampling="randomized breadth-first; topology only; not representative")
    cache.parent.mkdir(exist_ok=True, parents=True)
    sparse.save_npz(cache.with_suffix(".npz"), graph)
    np.save(cache.with_suffix(".npy"), selected)
    cache.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    return graph, selected, meta


def first_retweet_hours(events, node_ids):
    """Proxy adoption = actor's first RT. Being retweeted is NOT an activation."""
    first = events.loc[events.kind == "RT"].groupby("actor").hour.min()
    return first.reindex(node_ids).fillna(np.inf).to_numpy()


def cumulative_counts(first_hours, hours):
    """At boundary h, count first retweets strictly before h."""
    return np.searchsorted(np.sort(first_hours), hours, side="left")
