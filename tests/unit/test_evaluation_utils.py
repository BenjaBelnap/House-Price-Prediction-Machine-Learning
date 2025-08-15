import numpy as np

from src import evaluation_utils as eu
import pytest


@pytest.mark.unit
def test_evaluate_model_metrics():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.1, 1.9, 3.05])

    metrics = eu.evaluate_model(y_true, y_pred, "TestModel")
    assert set(metrics.keys()) == {"mae", "rmse", "r2"}
    assert isinstance(metrics["mae"], float)


@pytest.mark.unit
def test_plot_predictions_runs_without_error():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.1, 1.9, 3.05])
    eu.plot_predictions(y_true, y_pred, "TestModel")
