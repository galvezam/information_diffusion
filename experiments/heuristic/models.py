"""Two small synchronous, progressive diffusion models. A[u,v] means u influences v."""
import numpy as np


def simulate(graph, seeds, steps, model, parameter, rng):
    """Return active-user counts at step 0..steps; one step has no intrinsic hours.

    IC: newly active users get ONE attempt per outgoing edge, probability p.
    LT: fixed threshold per node ~ Uniform(0, 1); each incoming edge has weight
        scale / in_degree. With scale <= 1, incoming weights sum to <= 1.
    """
    if model not in {"IC", "LT"}:
        raise ValueError("model must be IC or LT")
    if not 0 <= parameter <= 1:
        raise ValueError("parameter must be between 0 and 1")
    active = np.asarray(seeds, dtype=bool).copy()
    if graph.shape != (len(active), len(active)) or steps < 0:
        raise ValueError("Graph, seeds, or steps have incompatible dimensions")
    frontier = np.flatnonzero(active)
    counts = np.empty(steps + 1, dtype=int)
    counts[0] = active.sum()
    incoming = graph.T.tocsr()
    degree = np.asarray(incoming.sum(axis=1)).ravel()
    thresholds = rng.random(len(active)) if model == "LT" else None
    for step in range(1, steps + 1):
        if model == "IC":
            targets = graph[frontier].indices
            successes = targets[rng.random(len(targets)) < parameter]
            frontier = np.unique(successes[~active[successes]])
        else:
            exposure = (incoming @ active.astype(float)) / np.maximum(degree, 1)
            frontier = np.flatnonzero(~active & (exposure > 0) & (parameter * exposure >= thresholds))
        active[frontier] = True
        counts[step] = active.sum()
        if len(frontier) == 0:
            counts[step:] = counts[step]
            break
    return counts


def ensemble(graph, seeds, hours, model, parameter, step_hours, runs=30, seed=1000):
    """Hours are elapsed from initialization; return runs x hourly boundaries."""
    if step_hours <= 0 or np.any(np.asarray(hours) < 0) or runs < 1:
        raise ValueError("Expected positive step_hours/runs and nonnegative hours")
    indices = np.floor(np.asarray(hours) / step_hours).astype(int)
    return np.array([simulate(graph, seeds, int(indices.max()), model, parameter,
                              np.random.default_rng(seed + i))[indices] for i in range(runs)])
