# GNN experiment

**Planned; no model has been trained and no results are reported yet.** This is the
next experiment. Its notebook, training code, runner, report (`gnn.html`), and
results will live here, independently of the heuristic report.

Start from the [GNN implementation plan](../heuristic/heuristic_models.html#gnn).
Reuse shared graph sampling and labels from `diffusion/data.py`, and cumulative
curve scoring from `diffusion/evaluation.py`. Begin with a small CPU model and one
or two numerical-library threads.

Use early data for training and validation. Report one-step predictions separately
from autonomous rollouts: one-step predictions use observed states, while a
rollout must feed its own simulated states forward from hour 24. Only the latter
matches the current heuristic continuation benchmark. Include a simple logistic
control and check calibration before sampling adoption trajectories.

The [preserved IC/LT benchmark](../heuristic/benchmark/README.md) provides reference
metrics, curves, and exact settings. Check that input hashes, node sample, split,
and forecast origin match before comparing. Keep model selection independent of
held-out labels; results-guided revisions on this already inspected week are
exploratory.

Once established, save a standalone `gnn.html` report and a compact benchmark
snapshot here for the [synthesis experiment](../synthesis/README.md).

[All experiments](../../README.md)
