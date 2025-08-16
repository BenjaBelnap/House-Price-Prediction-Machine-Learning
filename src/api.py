from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import time
import logging

app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices using trained models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
    # Pre-compute SalePrice histogram for insights if available
    saleprice_hist = None
    if 'SalePrice' in reference_data.columns:
        counts, bin_edges = np.histogram(reference_data['SalePrice'].dropna(), bins=20)
        centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        saleprice_hist = {
            'counts': counts.astype(int).tolist(),
            'bin_edges': bin_edges.astype(float).tolist(),
            'centers': centers.astype(float).tolist(),
        }
    print("Feature defaults calculated from reference data")
except Exception as e:
    print(f"Error loading reference data for defaults: {str(e)}")
    feature_defaults = {}  # Empty defaults if reference data can't be loaded
    saleprice_hist = None

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

# --- Basic logging and in-memory metrics for monitoring ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("house-price-api")

request_metrics: Dict[str, Any] = {
    'request_count': 0,
    'per_path': {},
    'prediction_count': 0,
    'last_prediction_ts': None,
}

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    path = request.url.path
    request_metrics['request_count'] += 1
    request_metrics['per_path'][path] = request_metrics['per_path'].get(path, 0) + 1
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    logger.info(f"%s %s -> %s in %dms", request.method, path, getattr(response, 'status_code', '200'), duration_ms)
    return response

@app.get("/")
async def root():
    """API root endpoint with basic info"""
    return {
        "message": "House Price Prediction API",
        "endpoints": {
            "GET /models": "List all available models",
            "POST /predict": "Make a house price prediction",
            "GET /features": "Get required features and their default values",
            "GET /insights": "Get histogram and summary insights for dashboard",
            "GET /health": "Health check",
            "GET /metrics": "Basic API metrics"
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

@app.get("/insights")
async def get_insights():
    """Return precomputed insights for visualizations (histogram, counts)."""
    feature_counts = {
        'numerical': len([col for col, val in feature_defaults.items() if isinstance(val, (int, float)) and not isinstance(val, bool)]),
        'categorical': len([col for col, val in feature_defaults.items() if isinstance(val, str)]),
    }
    best_model_name = None
    best_r2 = None
    try:
        best_model_name = min(
            models.items(),
            key=lambda x: x[1]['metadata']['metrics']['test']['mae'] 
                if 'test' in x[1]['metadata']['metrics'] 
                else x[1]['metadata']['metrics']['mae']
        )[0]
        metrics = models[best_model_name]['metadata']['metrics']
        best_r2 = (metrics.get('test') or {}).get('r2') or metrics.get('r2')
    except Exception:
        pass
    return {
        'feature_counts': feature_counts,
        'saleprice_histogram': saleprice_hist,
        'best_model': best_model_name,
        'best_model_r2': best_r2,
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
        
        # update metrics
        request_metrics['prediction_count'] += 1
        request_metrics['last_prediction_ts'] = time.time()

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

@app.get("/health")
async def health():
    """Simple health check endpoint."""
    return {
        'status': 'ok',
        'models_loaded': len(models),
        'has_reference_data': bool(feature_defaults),
    }

@app.get("/metrics")
async def metrics():
    """Return basic in-memory metrics for monitoring."""
    return request_metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
