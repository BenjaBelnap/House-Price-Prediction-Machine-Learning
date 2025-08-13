from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import pandas as pd

def get_default_models():
    """Return dictionary of default model configurations"""
    return {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    }

def debug_model_performance(model, X_train, X_test, y_train, y_test, model_name):
    """Debug model performance and print detailed analysis"""
    print(f"=== {model_name} Debug Report ===")
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    
    # Testing performance
    y_test_pred = model.predict(X_test)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print("\nPerformance Metrics:")
    print(f"Training MAE: ${train_mae:,.2f}")
    print(f"Testing MAE: ${test_mae:,.2f}")
    print(f"Training R²: {train_r2:.4f}")
    print(f"Testing R²: {test_r2:.4f}")
    
    # Check for overfitting
    print("\nOverfitting Analysis:")
    mae_diff = abs(train_mae - test_mae)
    r2_diff = abs(train_r2 - test_r2)
    print(f"MAE difference (train-test): ${mae_diff:,.2f}")
    print(f"R² difference (train-test): {r2_diff:.4f}")
    
    if mae_diff > 10000 or r2_diff > 0.1:
        print("WARNING: Possible overfitting detected!")
        
    # Feature importance for tree-based models
    if hasattr(model, 'feature_importances_'):
        print("\nTop 10 Important Features:")
        importances = pd.DataFrame({
            'feature': X_train.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(importances.head(10))
        
    return {
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_r2': train_r2,
        'test_r2': test_r2
    }
