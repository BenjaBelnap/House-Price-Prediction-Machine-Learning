import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def list_models():
    """Get list of available models and their metrics"""
    response = requests.get(f"{BASE_URL}/models")
    if response.status_code == 200:
        models = response.json()
        print("\nAvailable Models:")
        print("-" * 50)
        for name, info in models.items():
            print(f"\nModel: {name}")
            # print(f"Test MAE: ${info['metrics']['mae']:,.2f}")
            # print(f"Test RMSE: ${info['metrics']['rmse']:,.2f}")
            # print(f"Test R²: {info['metrics']['r2']:.4f}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def make_prediction(features, model_name=None):
    """Make a house price prediction"""
    payload = {
        "features": features,
        "model_name": model_name
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\nPrediction Results:")
        print("-" * 50)
        print(f"Predicted Price: ${result['predicted_price']:,.2f}")
        print(f"Model Used: {result['model_used']}")
        print("\nModel Metrics:")
        print(f"MAE: ${result['confidence_metrics']['train']['mae']:,.2f}")
        print(f"RMSE: ${result['confidence_metrics']['train']['rmse']:,.2f}")
        print(f"R²: {result['confidence_metrics']['train']['r2']:.4f}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # First, let's see what models are available
    list_models()
    
    # Example house features for prediction
    sample_features = {
        "LotArea": 8450,
        "YearBuilt": 2003,
        "1stFlrSF": 856,
        "2ndFlrSF": 854,
        "FullBath": 2,
        "BedroomAbvGr": 3,
        "TotRmsAbvGrd": 8,
        "GarageCars": 2,
        "GarageArea": 548,
        "OverallQual": 7,
        "OverallCond": 5,
        "GrLivArea": 1710,
        "TotalBsmtSF": 856
    }
    
    print("\nMaking prediction with default (best) model:")
    make_prediction(sample_features)
    
    print("\nMaking prediction with specific model (random_forest):")
    make_prediction(sample_features, model_name="random_forest")
