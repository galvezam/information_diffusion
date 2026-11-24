# Heuristic models: IC and LT

**Implemented.** Open [heuristic_models.html](heuristic_models.html) for the
standalone report, including the initialize → fit → test explanation in section 4.

- `analysis.ipynb`: experiment settings, explanations, and plots.
- `models.py`: independent cascade and linear threshold update rules.
- `experiment.py`: parameter search and continuation experiment.
- `run.py`: execute the notebook and render the report.
- [benchmark/](benchmark/README.md): preserved pre-GNN numerical results.
- `results/`: optional latest-run exports, ignored by Git.

From the project root:

```sh
uv run python experiments/heuristic/run.py
uv run python experiments/heuristic/run.py --export
```

From this folder, use `uv run python run.py` (optionally `--export`). Both use the
root virtual environment and shared data/cache. Rebuilding updates this report;
it never changes the preserved benchmark. IC/LT settings and stochastic behavior
are unchanged by the folder reorganization.

The default run uses 5,000 users, graph seed 42, initialization at hour 24,
fitting through hour 72, and evaluation through hour 168. LT fits the early period
better; IC has the lowest held-out cumulative RMSE in this sample. Read the report
for the limits of that comparison.

[All experiments](../../README.md) · [Next: GNN](../gnn/README.md)
