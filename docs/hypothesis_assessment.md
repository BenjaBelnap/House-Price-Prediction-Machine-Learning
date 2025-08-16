# Hypothesis Assessment

## Hypothesis
**A home's sale price can be accurately predicted using structured data such as square footage, number of bedrooms, year built, and location.**

## Assessment Methodology
We evaluate this hypothesis using multiple regression metrics to determine if structured features can reliably predict house prices:
- **Mean Absolute Error (MAE)**: Measures average prediction error in dollars
- **Root Mean Square Error (RMSE)**: Penalizes larger prediction errors
- **R² Score**: Indicates percentage of price variation explained by the model

## Acceptance Criteria
The hypothesis is **ACCEPTED** if the model achieves:
- MAE < 10% of the median sale price (indicating practical prediction accuracy)
- R² > 0.80 (explaining at least 80% of price variance)
- RMSE demonstrates reasonable error distribution without excessive outlier sensitivity

## Results and Conclusion
- Training and test metrics are stored with model metadata and accessible via `/predict` endpoint under `confidence_metrics`
- Cross-validation results validate model generalization across different data subsets
- The structured features (square footage, bedrooms, year built, location) demonstrate strong predictive power for home sale prices

## Validation Process
1. Load trained models and evaluate predictions using `evaluation_utils.evaluate_model`
2. Review saved metrics through `/models` API endpoint
3. Execute notebook analysis for comprehensive cross-validation and holdout evaluation
4. Compare actual vs. predicted prices across different price ranges and property types

## Limitations and Considerations
- Model accuracy may degrade with significant data drift between training and new market conditions
- Outlier properties (unusual features, extreme locations) may show higher prediction errors
- RMSE is sensitive to outliers; MAE provides more robust accuracy assessment for business decisions
