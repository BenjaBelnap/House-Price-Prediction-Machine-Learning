# Business Vision and Requirements

## Vision
Accelerate and standardize residential property valuation for a mortgage company by delivering a reliable, fast, and explainable price estimation product built on the Ames Housing dataset.

## Business Objectives
- Reduce appraisal turnaround time by >50% for preliminary valuation.
- Provide consistent, auditable estimates with explainability (top features).
- Achieve <10% Mean Absolute Percentage Error (proxy: R²/MAE thresholds) on holdout data.

## Success Metrics
- MAE (USD) and R² on test set.
- Adoption: # of estimates run per week.
- Latency: <400ms median prediction.

## Stakeholders
- Mortgage underwriting team
- Appraisers and QA reviewers
- Data science/engineering team

## Functional Requirements
- Web UI for entering property features and viewing predictions.
- API for programmatic access and integration.
- Defaults for missing features and feature-importance for transparency.
- Health/metrics endpoints for monitoring.

## Non-Functional Requirements
- Reliability: 99% API success for internal users.
- Security: CORS restrictions, input validation.
- Observability: basic metrics + logs.
- Maintainability: tests, versioned models, environment reproducibility (Poetry).
