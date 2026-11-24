"""Model-independent graph diagnostics and cumulative-curve evaluation."""
import numpy as np
import pandas as pd


def reachable_mask(graph, seeds):
    """Absolute ceiling for a closed, progressive model with no external arrivals."""
    reached = seeds.copy()
    while True:
        expanded = reached | (graph.T @ reached.astype(float) > 0)
        if np.array_equal(expanded, reached):
            return reached
        reached = expanded


def evaluate_curves(predictions, observed, hours, fit_end):
    """Score runs x hourly-boundary counts, holding out boundaries after fit_end.

    All models use the same observed curve, boundaries, and forecast origin.
    test_speed is a predicted rate, not a speed-error metric.
    """
    test = hours > fit_end
    metrics = []
    for model, curves in predictions.items():
        mean = curves.mean(axis=0)
        metrics.append(dict(model=model,
            test_rmse=float(np.sqrt(np.mean((mean[test] - observed[test]) ** 2))),
            test_mae=float(np.mean(np.abs(mean[test] - observed[test]))),
            final_error=float(mean[-1] - observed[-1]),
            test_speed=float((mean[-1] - mean[hours == fit_end][0]) / (hours[-1] - fit_end))))
    return pd.DataFrame(metrics)
