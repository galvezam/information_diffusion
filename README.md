# Higgs diffusion experiments

Explore each experiment in its own folder. Reports embed their figures and can be
opened locally without installing anything.

- **[Heuristic models: IC and LT](experiments/heuristic/README.md)** — implemented.
  Open [heuristic_models.html](experiments/heuristic/heuristic_models.html) for the
  dataset, model mechanics, results, and limitations. A preserved
  [benchmark](experiments/heuristic/benchmark/README.md) holds the pre-GNN numbers.
- **[GNN](experiments/gnn/README.md)** — next experiment; not implemented yet.
- **[Prompted agents](experiments/prompted_agents/README.md)** — planned.
- **[Synthesis](experiments/synthesis/README.md)** — planned comparison of all three
  model families once their individual experiments are established.

## Run the heuristic experiment

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required to regenerate results.
Run from the project root:

```sh
uv sync --locked
uv run python experiments/heuristic/run.py
```

This uses the project's virtual environment and rebuilds only
`experiments/heuristic/heuristic_models.html`. The original `uv run python run.py`
command remains a shortcut. The runner uses one process and one numerical-library
thread by default, with no GPU or API key. Unchanged graph samples reuse `.cache/`.

For PNGs, CSVs, simulation draws, and a reproducibility manifest:

```sh
uv run python experiments/heuristic/run.py --export
```

Exports go to ignored `experiments/heuristic/results/` and are overwritten by the
next export. The tracked `experiments/heuristic/benchmark/` snapshot is separate
and is never overwritten by the runner. The notebook keeps empty outputs; the
HTML is the rendered result. Select the root `.venv/bin/python` kernel to edit the
notebook interactively from the root or the experiment directory.

## Shared code and data

```text
experiments/heuristic/       IC/LT notebook, models, tuning, runner, report, benchmark
experiments/gnn/             Learned-model experiment
experiments/prompted_agents/ Prompted-agent experiment
experiments/synthesis/       Cross-family comparison experiment
diffusion/data.py           Shared graph sampling and adoption labels
diffusion/evaluation.py     Shared curve scoring and reachability
data/                      Original compressed datasets (not tracked)
docs/                      Original proposal PDF and Word document
pyproject.toml + uv.lock    One reproducible virtual environment
```

Keep model-specific training, simulation, plots, and reports with their experiment.
Reuse `diffusion/` for model-independent functions. Experiments can import another
family's implementation when they need a control; avoid copying model code.

All curves use the same contract: a sparse source-to-recipient graph, a fixed node
ordering, first-RT adoption labels, and simulation counts shaped
`(runs, hourly_boundaries)`. `diffusion.evaluation.evaluate_curves` scores the
ensemble mean against observed cumulative counts. The baseline initializes at
hour 24, fits boundaries 25–72, and tests boundaries 73–168 without injecting later
observations into the simulated state. Future comparisons must explicitly match
sample, split, forecast origin, and available information.

## Dataset setup

Download these three files from [SNAP](https://snap.stanford.edu/data/higgs-twitter.html)
into `data/`, keeping the `.gz` compression:

- `higgs-activity_time.txt.gz`
- `higgs-social_network.edgelist.gz`
- `higgs-retweet_network.edgelist.gz`

They are already present in this working copy. They cover July 1–7, **2012**;
2015 is the dataset update date. Raw data, environments, caches, and optional
exports are excluded from Git. Reports and compact benchmark snapshots are kept
with their experiments. Rebuilding the heuristic report is the end-to-end check.
