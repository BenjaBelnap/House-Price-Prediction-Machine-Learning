# Analysis and Product Construction

This document points to the exact code used for descriptive and predictive modeling and explains the flow.

## Code Map
- Data prep utilities: `src/data_preprocessing.py`
- Modeling utilities: `src/model_utils.py`
- Evaluation utilities: `src/evaluation_utils.py`
- API serving the product: `src/api.py`
- Frontend UI: `frontend/` (FastAPI static server + HTML/CSS/JS)
- Example API usage: `examples/api_usage_example.py`
- Notebook exploration and training: `notebooks/house_price_prediction.ipynb`

## Descriptive Components
- Summary, quality checks, and missing-value handling (`check_data_quality`, `prepare_data`).
- Metrics and plots: MAE, RMSE, R² via `evaluation_utils.evaluate_model` and `plot_predictions`.
- Feature importance exposed through `/features` endpoint and visualized in the dashboard.

## Predictive Components
- Baselines and candidates: RandomForest, XGBoost (`model_utils.get_default_models`).
- Trained artifacts stored under `models/` and loaded in `src/api.py`.
- `/predict` endpoint accepts partial features, fills defaults, and returns price + confidence.

## Serving and Interactivity
- FastAPI service (`src/api.py`): `/`, `/models`, `/features`, `/predict`, `/insights`, `/health`, `/metrics`.
- Frontend renders forms dynamically from `/features` and charts from `/insights`.
