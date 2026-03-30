import pandas as pd
import joblib
import os

def load_data(filepath='streamlit_data.csv'):
    """
    Reads the streamlit_data.csv file.
    Includes basic error handling if the file is missing or corrupted.
    """
    if not os.path.exists(filepath):
        print(f"Warning: '{filepath}' not found. Please ensure the notebook cell was run.")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return pd.DataFrame()

def predict_score(price, freight, delivery_days):
    """
    Loads the Random Forest model and feature column list,
    constructs an input feature array, and predicts the review score.
    Returns the predicted score, or None if files are missing.
    """
    model_path = 'rf_model.pkl.z'
    features_path = 'features.pkl'
    
    if not os.path.exists(model_path):
        print(f"Warning: '{model_path}' not found. Cannot predict.")
        return None
        
    if not os.path.exists(features_path):
        print(f"Warning: '{features_path}' not found. Cannot construct features.")
        return None
        
    try:
        # Load the model and feature names
        rf_model = joblib.load(model_path)
        features = joblib.load(features_path)
        
        # Build the input dictionary dynamically using the expected terms to 
        # ensure we match the exact column names saved in features.pkl
        input_data = {}
        for feat in features:
            f_lower = feat.lower()
            if 'price' in f_lower:
                input_data[feat] = price
            elif 'freight' in f_lower:
                input_data[feat] = freight
            elif 'delivery' in f_lower or 'delay' in f_lower or 'days' in f_lower:
                input_data[feat] = delivery_days
            else:
                input_data[feat] = 0  # Fallback for any unknown features
                
        # Create a single-row DataFrame ensuring columns match exactly
        df_input = pd.DataFrame([input_data], columns=features)
        
        # Predict and return the result
        prediction = rf_model.predict(df_input)
        return prediction[0]
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None
