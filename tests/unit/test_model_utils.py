import numpy as np
import pandas as pd

from src import model_utils as mu
import pytest


def test_get_default_models_contains_expected_keys():
    models = mu.get_default_models()
    # XGBoost import may fail in some environments; accept presence of RF at minimum
    assert "Random Forest" in models


def test_debug_model_performance_returns_metrics():
    # Tiny synthetic dataset
    X_train = pd.DataFrame({"a": [1, 2, 3], "b": [0, 1, 0]})
    y_train = np.array([1.0, 2.0, 3.0])
    X_test = pd.DataFrame({"a": [4, 5], "b": [1, 0]})
    y_test = np.array([4.0, 5.0])

    model = mu.get_default_models()["Random Forest"]
    model.random_state = 42
    model.fit(X_train, y_train)

    metrics = mu.debug_model_performance(model, X_train, X_test, y_train, y_test, "Random Forest")

    assert {"train_mae", "test_mae", "train_r2", "test_r2"}.issubset(metrics.keys())
    assert isinstance(metrics["train_mae"], float)
