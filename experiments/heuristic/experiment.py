"""Fit on the early curve, freeze choices, and score the later continuation."""
import numpy as np
import pandas as pd

from diffusion.data import cumulative_counts
from diffusion.evaluation import evaluate_curves, reachable_mask
from .models import ensemble

PARAMETERS = {"IC": [0, .001, .003, .01, .03, .1, .3, 1.0],
              "LT": [0, .05, .1, .2, .4, .6, .8, 1.0]}


def run_experiment(graph, first_hours, seed_hour=24, fit_end=72, end_hour=168,
                   fit_runs=10, runs=50, random_seed=42):
    """Single chronological split, no held-out data in selection.

    All users observed before seed_hour initialize the process; for IC they each
    get one fresh attempt. This is a snapshot approximation, not inferred history.
    Fitting uses (seed_hour, fit_end]; evaluation uses (fit_end, end_hour].
    Simulation continues from the same initialization, never reseeded on test data.
    """
    if not 0 < seed_hour < fit_end < end_hour:
        raise ValueError("Require 0 < seed_hour < fit_end < end_hour")
    hours = np.arange(seed_hour, end_hour + 1)
    observed = cumulative_counts(first_hours, hours)
    seeds = first_hours < seed_hour
    if not seeds.any():
        raise ValueError("No early retweeters in this sample; increase n_nodes or seed_hour.")
    fit = (hours > seed_hour) & (hours <= fit_end)
    rows, predictions = [], {}
    for model, parameters in PARAMETERS.items():
        for step_hours in (1, 3, 6, 12):
            for parameter in parameters:
                curves = ensemble(graph, seeds, hours[fit] - seed_hour, model, parameter,
                                  step_hours, fit_runs, random_seed)
                rmse = np.sqrt(np.mean((curves.mean(axis=0) - observed[fit]) ** 2))
                rows.append(dict(model=model, parameter=parameter, step_hours=step_hours, fit_rmse=rmse))
    tuning = pd.DataFrame(rows)
    best = tuning.loc[tuning.groupby("model").fit_rmse.idxmin()].reset_index(drop=True)
    for row in best.itertuples():
        predictions[row.model] = ensemble(graph, seeds, hours - seed_hour, row.model,
                                          row.parameter, row.step_hours, runs, random_seed + 10000)
    predictions["No growth"] = np.full((1, len(hours)), observed[0])
    # Simple trend baseline: its rate uses only the fitting period.
    rate = (observed[hours == fit_end][0] - observed[0]) / (fit_end - seed_hour)
    predictions["Linear trend"] = np.minimum(len(seeds), observed[0] + rate * (hours - seed_hour))[None, :]
    metrics = evaluate_curves(predictions, observed, hours, fit_end)
    return dict(hours=hours, observed=observed, seeds=seeds, fit_end=fit_end,
                seed_hour=seed_hour, predictions=predictions, tuning=tuning, best=best,
                metrics=metrics, reachable=reachable_mask(graph, seeds),
                observed_test_speed=float((observed[-1] - observed[hours == fit_end][0]) / (end_hour - fit_end)))
