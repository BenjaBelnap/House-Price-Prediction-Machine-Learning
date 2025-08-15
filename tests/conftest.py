import importlib
import sys
from typing import List

import pandas as pd
import numpy as np
import pytest


class FakeModel:
    """A simple fake model with optional feature importances and configurable predict."""

    def __init__(self, name: str, return_value: float, feature_names: List[str], importances: List[float] | None = None):
        self.name = name
        self._return_value = float(return_value)
        self._feature_names = feature_names
        if importances is not None:
            # attach attribute to mimic tree-based models
            import numpy as _np
            self.feature_importances_ = _np.array(importances, dtype=float)

    def predict(self, X):
        # Return a constant prediction regardless of input for determinism
        import numpy as _np
        return _np.array([self._return_value] * len(X))


@pytest.fixture()
def fake_data_df():
    """Small DataFrame to simulate reference CSV for feature defaults."""
    return pd.DataFrame(
        {
            "LotArea": [8000, 9000, 10000, 11000, np.nan],
            "YearBuilt": [1990, 2000, 2010, np.nan, 2005],
            "GrLivArea": [1500, 1600, 1700, 1800, 1900],
            "Neighborhood": ["NAmes", "CollgCr", "NAmes", "Edwards", "NAmes"],
            "SalePrice": [150000, 180000, 200000, 220000, 210000],
        }
    )


@pytest.fixture()
def fake_models_fs(monkeypatch, fake_data_df):
    """Monkeypatch filesystem and loaders so importing src.api uses fake models and data."""

    # Fake files in models dir
    def fake_listdir(path):
        # Two models present
        return ["random_forest.joblib", "xgboost.joblib"]

    monkeypatch.setattr("os.listdir", fake_listdir)

    feature_names = ["LotArea", "YearBuilt", "GrLivArea"]

    # Create two fake models with different metrics
    rf_model = FakeModel(
        name="random_forest",
        return_value=200000.0,
        feature_names=feature_names,
        importances=[0.6, 0.3, 0.1],
    )
    xgb_model = FakeModel(
        name="xgboost",
        return_value=150000.0,
        feature_names=feature_names,
        importances=None,
    )

    # joblib.load behavior depends on path
    def fake_joblib_load(path):
        path_str = str(path)
        if path_str.endswith("random_forest.joblib") and "_metadata" not in path_str:
            return rf_model
        if path_str.endswith("xgboost.joblib") and "_metadata" not in path_str:
            return xgb_model
        if path_str.endswith("random_forest_metadata.joblib"):
            return {
                "metrics": {"test": {"mae": 1000.0, "rmse": 1200.0, "r2": 0.9}},
                "features": feature_names,
            }
        if path_str.endswith("xgboost_metadata.joblib"):
            # flat metrics to exercise both paths
            return {"metrics": {"mae": 2000.0, "rmse": 2200.0, "r2": 0.85}, "features": feature_names}
        # Default return for any unexpected path
        raise FileNotFoundError(path_str)

    monkeypatch.setattr("joblib.load", fake_joblib_load)

    # Patch pandas.read_csv used for defaults in src.api
    def fake_read_csv(_):
        return fake_data_df.copy()

    monkeypatch.setattr("pandas.read_csv", lambda *args, **kwargs: fake_read_csv(args[0]))

    return {
        "rf_model": rf_model,
        "xgb_model": xgb_model,
        "feature_names": feature_names,
    }


@pytest.fixture()
def api_module(fake_models_fs):
    """Import src.api with monkeypatched environment and return the module object.

    Reload per test to isolate global state since src.api runs loaders at import time.
    """
    # Ensure fresh import each time
    if "src.api" in sys.modules:
        del sys.modules["src.api"]
    importlib.invalidate_caches()
    module = importlib.import_module("src.api")
    try:
        yield module
    finally:
        # Clean up to avoid shared state between tests
        if "src.api" in sys.modules:
            del sys.modules["src.api"]
        importlib.invalidate_caches()


@pytest.fixture()
def api_client(api_module):
    from fastapi.testclient import TestClient

    return TestClient(api_module.app)


@pytest.fixture(autouse=True)
def matplotlib_agg_backend(monkeypatch):
    """Force non-interactive backend for plotting tests."""
    import matplotlib

    matplotlib.use("Agg", force=True)
    yield
