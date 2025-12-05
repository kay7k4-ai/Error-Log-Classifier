import os, sys, joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from src.preprocessor import read_logs
from src.preprocessing.cleaner import clean_logs
from src.model.vectorizer import fit_vectorizer

def assign_labels(raw_logs):
    labels = []
    for l in raw_logs:
        s = (l or "").lower()
        if "critical" in s:
            labels.append("CRITICAL")
        elif "error" in s:
            labels.append("ERROR")
        elif "warning" in s:
            labels.append("WARNING")
        elif "info" in s:
            labels.append("INFO")
        else:
            labels.append("UNKNOWN")
    return labels

if __name__ == "__main__":
    print("Training model...")

    data_path = os.path.join(PROJECT_ROOT, "data", "sample_logs.txt")
    raw_logs = read_logs(data_path)
    if not raw_logs:
        print("No logs found at", data_path)
        raise SystemExit(1)

    cleaned = clean_logs(raw_logs)
    labels = assign_labels(raw_logs)

    vectorizer, X = fit_vectorizer(cleaned, max_features=4000)

    # Filter lines and labels where label is not UNKNOWN to improve training signal
    X_list = []
    y_list = []
    for vec_row, lbl in zip(cleaned, labels):
        if lbl != "UNKNOWN":
            X_list.append(vec_row)
            y_list.append(lbl)

    if not X_list:
        print("No labeled examples found (all UNKNOWN). Add more labeled data.")
        raise SystemExit(1)

    # Vectorize again on filtered data
    vectorizer, X = fit_vectorizer(X_list)
    X_train, X_test, y_train, y_test = train_test_split(X, y_list, test_size=0.2, random_state=42)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc*100:.2f}%")

    model_path = os.path.join(PROJECT_ROOT, "model.pkl")
    vec_path = os.path.join(PROJECT_ROOT, "vectorizer.pkl")
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    print("Saved model to", model_path)
    print("Saved vectorizer to", vec_path)
