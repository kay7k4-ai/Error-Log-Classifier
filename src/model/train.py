import os
import sys
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# -------------------------------------------------------
# FIX PATHS
# -------------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from src.preprocessor import read_logs
from src.preprocessing.cleaner import clean_logs
from src.model.vectorizer import fit_vectorizer


# -------------------------------------------------------
# TEMPORARY LABELING FUNCTION
# (We label logs using simple keywords to train ML)
# -------------------------------------------------------
def assign_labels(cleaned_logs):
    labels = []
    for line in cleaned_logs:
        if "error" in line:
            labels.append("ERROR")
        elif "warning" in line:
            labels.append("WARNING")
        elif "critical" in line:
            labels.append("CRITICAL")
        elif "info" in line:
            labels.append("INFO")
        else:
            labels.append("UNKNOWN")
    return labels


# -------------------------------------------------------
# MAIN TRAINING PIPELINE
# -------------------------------------------------------
if __name__ == "__main__":

    print("\n=== TRAINING ERROR LOG CLASSIFIER ===")

    # Load raw logs
    log_path = os.path.join(PROJECT_ROOT, "data", "sample_logs.txt")
    raw_logs = read_logs(log_path)

    # Clean logs
    cleaned_logs = clean_logs(raw_logs)

    # Auto-generate labels
    labels = assign_labels(cleaned_logs)

    # TF-IDF vectorization
    vectorizer, X = fit_vectorizer(cleaned_logs)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.25, random_state=42
    )

    # Train Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Test model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\nTraining complete!")
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Save model + vectorizer
    model_path = os.path.join(PROJECT_ROOT, "model.pkl")
    vec_path = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    print("\nSaved:")
    print(f"- Model: {model_path}")
    print(f"- Vectorizer: {vec_path}")
