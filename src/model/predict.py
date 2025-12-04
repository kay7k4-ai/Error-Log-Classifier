import os
import sys
import joblib

# FIX PATHS
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from src.preprocessing.cleaner import clean_logs

# LOAD MODEL + VECTORIZER
MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")
VEC_PATH = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

# PREDICT FUNCTION
def predict_log(log_text):
    """
    Predict the category of a single log line.
    """

    # 1. Clean text
    cleaned = clean_logs([log_text])

    # 2. Convert to TF-IDF
    vector = vectorizer.transform(cleaned)

    # 3. Predict
    prediction = model.predict(vector)[0]

    return prediction

# TESTING (Run this file directly)
if __name__ == "__main__":

    print("\n=== TESTING PREDICTOR ===")

    sample = "2024-10-21 10:44:22 - WARNING - Low disk space detected"

    result = predict_log(sample)

    print(f"Log: {sample}")
    print("Predicted Category:", result)
