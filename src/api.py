from fastapi import FastAPI, HTTPException
import joblib
import os
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Dict, List, Optional, Any

app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices using trained models",
    version="1.0.0"
)

# Load models
models = {}
models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

# Load reference dataset for defaults
try:
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'amesHousing.csv')
    reference_data = pd.read_csv(data_path)
    # Drop ID columns
    if 'PID' in reference_data.columns:
        reference_data = reference_data.drop(['PID', 'Order'], axis=1)
    
    # Calculate defaults for each column
    feature_defaults = {}
    
    # For numerical columns, use median
    numerical_cols = reference_data.select_dtypes(include=['int64', 'float64']).columns
    for col in numerical_cols:
        if col != 'SalePrice':  # Skip the target variable
            feature_defaults[col] = float(reference_data[col].median())
    
    # For categorical columns, use mode
    categorical_cols = reference_data.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        feature_defaults[col] = reference_data[col].mode()[0]
    
    print("Feature defaults calculated from reference data")
except Exception as e:
    print(f"Error loading reference data for defaults: {str(e)}")
    feature_defaults = {}  # Empty defaults if reference data can't be loaded

# Load trained models
try:
    for file in os.listdir(models_dir):
        if file.endswith('.joblib') and not file.endswith('_metadata.joblib'):
            model_name = file.replace('.joblib', '')
            model_path = os.path.join(models_dir, file)
            metadata_path = os.path.join(models_dir, f"{model_name}_metadata.joblib")
            
            models[model_name] = {
                'model': joblib.load(model_path),
                'metadata': joblib.load(metadata_path)
            }
    print(f"Loaded {len(models)} models from {models_dir}")
except Exception as e:
    print(f"Error loading models: {str(e)}")

class PredictionRequest(BaseModel):
    features: Dict[str, Any]
    model_name: Optional[str] = None

class PredictionResponse(BaseModel):
    predicted_price: float
    model_used: str
    confidence_metrics: Dict[str, Any]
    features_used: Dict[str, Any]
    missing_features: List[str]

@app.get("/")
async def root():
    """API root endpoint with basic info"""
    return {
        "message": "House Price Prediction API",
        "endpoints": {
            "GET /models": "List all available models",
            "POST /predict": "Make a house price prediction",
            "GET /features": "Get required features and their default values"
        }
    }

@app.get("/models")
async def list_models():
    """List all available models and their performance metrics"""
    return {
        name: {
            "metrics": model['metadata']['metrics'],
            "features": model['metadata']['features']
        }
        for name, model in models.items()
    }

@app.get("/features")
async def get_features():
    """Get list of all features, their default values, and importance rankings"""
    # Get feature importance from the best model
    best_model_name = min(
        models.items(),
        key=lambda x: x[1]['metadata']['metrics']['test']['mae'] 
            if 'test' in x[1]['metadata']['metrics'] 
            else x[1]['metadata']['metrics']['mae']
    )[0]
    
    feature_importance = {}
    if best_model_name in models:
        model_info = models[best_model_name]
        if hasattr(model_info['model'], 'feature_importances_'):
            importances = model_info['model'].feature_importances_
            feature_names = model_info['metadata']['features']
            
            # Create importance dictionary
            importance_dict = dict(zip(feature_names, importances))
            
            # Sort by importance and get top features
            sorted_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
            
            for i, (feature, importance) in enumerate(sorted_features):
                feature_importance[feature] = {
                    'importance': float(importance),
                    'rank': i + 1,
                    'is_top_10': i < 10
                }
    
    return {
        "feature_defaults": feature_defaults,
        "feature_importance": feature_importance,
        "numerical_features": [col for col in feature_defaults.keys() 
                             if isinstance(feature_defaults[col], (int, float)) 
                             and not isinstance(feature_defaults[col], bool)],
        "categorical_features": [col for col in feature_defaults.keys() 
                               if isinstance(feature_defaults[col], str)],
        "top_features": [f[0] for f in sorted(feature_importance.items(), 
                                            key=lambda x: x[1]['importance'], 
                                            reverse=True)[:10]] if feature_importance else []
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a house price prediction with optional features"""
    # If no model specified, use the one with best test MAE
    if request.model_name is None:
        request.model_name = min(
            models.items(),
            key=lambda x: x[1]['metadata']['metrics']['test']['mae'] 
                if 'test' in x[1]['metadata']['metrics'] 
                else x[1]['metadata']['metrics']['mae']
        )[0]
    
    if request.model_name not in models:
        raise HTTPException(
            status_code=404,
            detail=f"Model {request.model_name} not found"
        )
    
    model_info = models[request.model_name]
    required_features = model_info['metadata']['features']
    provided_features = set(request.features.keys())
    
    # Identify missing features
    missing_features = [f for f in required_features if f not in provided_features]
    
    # Create input data with defaults for missing values
    input_data = {}
    for feature in required_features:
        if feature in request.features:
            input_data[feature] = request.features[feature]
        elif feature in feature_defaults:
            input_data[feature] = feature_defaults[feature]
        else:
            # For categorical features encoded as dummies, default to 0
            if feature.find('_') > 0:  # Likely a dummy variable
                input_data[feature] = 0
            else:
                input_data[feature] = 0  # Default numerical to 0 if no median available
    
    # Create feature vector
    X = pd.DataFrame([input_data])
    
    # Ensure we have all needed columns in the right order
    for col in required_features:
        if col not in X.columns:
            X[col] = 0
    X = X[required_features]  # Reorder columns to match model expectations
    
    # Make prediction
    try:
        prediction = model_info['model'].predict(X)[0]
        
        return PredictionResponse(
            predicted_price=float(prediction),
            model_used=request.model_name,
            confidence_metrics=model_info['metadata']['metrics'],
            features_used=input_data,
            missing_features=missing_features
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
