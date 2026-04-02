import joblib
import pandas as pd
import os

# Update these paths to look at the root 'models' folder
MODEL_PATH = "models/predict_freight_model.pkl"
FEATURES_PATH = "models/freight_features.pkl"

def predict_freight_cost(input_data):
    # Load model
    with open(MODEL_PATH, "rb") as f:
        model = joblib.load(f)
    
    
    with open(FEATURES_PATH, "rb") as f:
        feature_names = joblib.load(f)

    input_df = pd.DataFrame(input_data)
    input_df = input_df[feature_names] 
    
    input_df['Predicted_Freight'] = model.predict(input_df).round()
    return input_df