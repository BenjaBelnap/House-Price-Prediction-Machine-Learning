from typing import Any, Dict

import pytest


@pytest.mark.unit
@pytest.mark.parametrize("path", ["/", "/models", "/features"])
def test_basic_endpoints_respond(api_client, path):
    resp = api_client.get(path)
    assert resp.status_code == 200


@pytest.mark.unit
def test_models_lists_available_models(api_client):
    data = api_client.get("/models").json()
    assert "random_forest" in data or "xgboost" in data or len(data) >= 1
    # Validate structure for one model
    any_model = next(iter(data.values()))
    assert "metrics" in any_model and "features" in any_model


@pytest.mark.unit
def test_features_returns_defaults_and_importance(api_client):
    data = api_client.get("/features").json()
    assert "feature_defaults" in data
    assert "numerical_features" in data
    assert isinstance(data["numerical_features"], list)


@pytest.mark.unit
def test_predict_default_model_selection(api_client):
    payload: Dict[str, Any] = {
        "features": {"LotArea": 9000, "YearBuilt": 2000, "GrLivArea": 1600}
    }
    resp = api_client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "predicted_price" in body and isinstance(body["predicted_price"], (int, float))
    assert "model_used" in body and isinstance(body["model_used"], str)


@pytest.mark.unit
def test_predict_with_specific_model_and_missing_features(api_client):
    payload = {"features": {"LotArea": 9000}, "model_name": "random_forest"}
    resp = api_client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert set(["predicted_price", "model_used", "confidence_metrics", "features_used", "missing_features"]) <= set(body.keys())
    assert "YearBuilt" in body["missing_features"] or "GrLivArea" in body["missing_features"]


@pytest.mark.unit
def test_predict_bad_model_name_404(api_client):
    payload = {"features": {"LotArea": 9000}, "model_name": "does_not_exist"}
    resp = api_client.post("/predict", json=payload)
    assert resp.status_code == 404
