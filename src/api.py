from fastapi import FastAPI, HTTPException
import joblib
import os
import pandas as pd
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
    print(models)
except Exception as e:
    print(f"Error loading models: {str(e)}")

class PredictionRequest(BaseModel):
    features: Dict[str, float]
    model_name: Optional[str] = None

class PredictionResponse(BaseModel):
    predicted_price: float
    model_used: str
    confidence_metrics: Dict[str, Any]

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

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a house price prediction"""
    # If no model specified, use the one with best test MAE
    if request.model_name is None:
        request.model_name = min(
            models.items(),
            key=lambda x: x[1]['metadata']['metrics']['test']['mae']
        )[0]
    
    if request.model_name not in models:
        raise HTTPException(
            status_code=404,
            detail=f"Model {request.model_name} not found"
        )
    
    model_info = models[request.model_name]
    required_features = set(model_info['metadata']['features'])
    provided_features = set(request.features.keys())
    

    
    # Create feature vector
    X = pd.DataFrame([request.features])
    for col in model_info['metadata']['features']:
        if col not in X.columns:
            X[col] = 0
    X = X[model_info['metadata']['features']]

    
    # Make prediction
    try:
        prediction = model_info['model'].predict(X)[0]
        
        return PredictionResponse(
            predicted_price=float(prediction),
            model_used=request.model_name,
            confidence_metrics=model_info['metadata']['metrics']
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
