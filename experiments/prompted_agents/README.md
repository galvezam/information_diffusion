# Prompted-agent experiment

**Planned; no agent simulations or results yet.** Keep the future simulation code,
notebook, prompts, runner, report (`prompted_agents.html`), and results in this folder.

Start from the [prompted-agent plan](../heuristic/heuristic_models.html#agents).
Begin with 20–50 nodes, a short horizon, and an explicit cost budget. Personas and
messages are synthetic because the dataset contains neither text nor profiles.
Record prompts, model versions, responses, retry behavior, token use, and cost.

Reuse shared data and scoring from `diffusion/`. Apply decisions synchronously and
keep adoption permanent. Declare whether external news can cause adoption without
an active neighbor. Compare IC/LT and the learned model on the same small graph
and information assumptions; the 5,000-user baseline is context, not a directly
matched benchmark for a smaller experiment.

Once established, save a standalone report and a compact benchmark snapshot for
the [synthesis experiment](../synthesis/README.md).

[All experiments](../../README.md)
