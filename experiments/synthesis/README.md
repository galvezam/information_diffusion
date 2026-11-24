# Synthesis: compare the three model families

**Planned; wait until the heuristic, GNN, and prompted-agent experiments are
established.** This folder will own the comparison notebook, runner, and
`synthesis.html` report. IC and LT are two baselines within the heuristic family.

Each individual report explains its own experiment. This report will compare all
three families under a common protocol:

- Same graph sample and node ordering, input fingerprints, adoption labels, and
  time boundaries.
- Same initial adopters and forecast origin; compare autonomous rollouts with
  autonomous rollouts. Present one-step prediction separately.
- Explicitly comparable access to external news, observed states, and other inputs.
- Shared cumulative RMSE, MAE, final-size error, spread-speed curves, milestones,
  and simulation-percentile bands, plus runtime and agent cost where relevant.
- Repeated graph samples and simulation runs before broad conclusions.

Import implementations from the experiment packages and shared evaluation from
`diffusion/`. Load preserved benchmark files only when their manifests establish
that the protocols match; otherwise rerun the families on a common configuration.
For a small prompted-agent pilot, rerun IC/LT and GNN on that same graph instead
of ranking its scores against the 5,000-user baseline.

The [heuristic benchmark](../heuristic/benchmark/README.md) is the first preserved
reference. The current held-out week has already been inspected; distinguish
exploratory comparisons from any new, predeclared evaluation.

[All experiments](../../README.md)
