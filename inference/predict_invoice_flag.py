import joblib
import pandas as pd
import os

# Using absolute path logic to prevent "File Not Found" errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "predict_flag_invoice.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")

def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def predict_invoice_flag(input_data):
    """
    Predicts if an invoice should be flagged.
    """
    model, scaler = load_artifacts()
    input_df = pd.DataFrame(input_data)
    
    # Scale the features
    input_scaled = scaler.transform(input_df)
    
    predictions = model.predict(input_scaled)
    
    # CHANGE THIS LINE from 'Is_Flagged' to 'Predicted_Flag'
    input_df['Predicted_Flag'] = predictions 
    
    return input_df

if __name__ == "__main__":
    # Local test data
    test_data = {
        "invoice_quantity": [50],
        "invoice_dollars": [1200],
        "Freight": [50],
        "total_item_quantity": [50],
        "total_item_dollars": [1200]
    }
    print(predict_invoice_flag(test_data))