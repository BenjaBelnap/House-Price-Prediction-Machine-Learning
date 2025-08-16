# Accuracy Assessment

We assess predictive accuracy using MAE.

## What is Reported
- Training and Test metrics stored with the model metadata and returned by `/predict` → `confidence_metrics`.
- Threshold: success if MAE < 10% of target scale.

## How to Reproduce
1. Load models and evaluate predictions using `evaluation_utils.evaluate_model`.
2. Inspect `/models` endpoint for the saved metrics.
3. Use the notebook to rerun cross-validation or holdout evaluation.

## Caveats
- Data drift between training and new data can degrade accuracy.
- Outliers heavily influence RMSE; prefer MAE for business reporting, with R² as a complement.
