# Preserved heuristic benchmark — before GNN work

Snapshot preserved on November 19, 2026. The folder reorganization reproduced
both original result tables and all ten embedded report figures exactly. The
[heuristic report](../heuristic_models.html) explains this run in detail.

These files are intentionally tracked and are **never overwritten by the report
runner**. Keep them unchanged when building GNN or prompted-agent experiments.
Store a later benchmark in a separately named snapshot instead.

- `metrics.csv`: held-out cumulative RMSE/MAE, final adoption error, and mean
  held-out spread speed for IC, LT, no growth, and linear trend.
- `curves.csv`: observed hourly cumulative adoption, the held-out mask, and each
  model's mean, 10th percentile, and 90th percentile curves.
- `selected_parameters.csv`: each heuristic model's selected parameter, hours per
  step, and early fitting error.
- `parameter_search.csv`: all candidate settings and early fitting errors.
- `milestones.csv`: first times the mean curves reach common adoption milestones.
- `manifest.json`: configuration, graph description, input and source SHA-256
  fingerprints, and numerical package versions.

The configuration is 5,000 users, graph seed 42, initialization at hour 24, fitting
through hour 72, and testing through hour 168, with 10 draws per candidate and
50 fresh draws per selected model. IC's held-out cumulative RMSE is 792.8814
users; LT's is 1891.3805. LT has the lower early fitting error. These numbers are
one graph sample and one temporal split, not a general model ranking.

Use the full-precision CSV values for comparisons, not rounded numbers from the
report. `test_speed` is a predicted average rate, not an error score. Its observed
reference can be computed from `curves.csv` as `(observed[168] - observed[72]) / 96`.
The percentile bands describe simulation randomness only.

Before using this benchmark, match input hashes, sample size/seed and ordering,
adoption definition, split, forecast origin, and access to observations. This is
an autonomous continuation from hour 24, not repeated one-step predictions using
true later states. Source hashes identify the code at snapshot creation; future
shared-code changes require rechecking comparability.

Full simulation draws and PNG exports remain in ignored `../results/` locally and
can be regenerated with `uv run python experiments/heuristic/run.py --export`
from the root. Only these compact comparison artifacts are part of the snapshot.
