import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

# FIX IMPORT PATHS
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

from src.preprocessor import read_logs
from src.preprocessing.cleaner import clean_logs

# VECTORIZER FUNCTIONS
def build_vectorizer():
    return TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1
    )


def fit_vectorizer(cleaned_logs):
    vectorizer = build_vectorizer()
    X = vectorizer.fit_transform(cleaned_logs)
    return vectorizer, X


def transform_new_logs(vectorizer, logs):
    return vectorizer.transform(logs)

# TESTING (Run with ▶️ or python src/model/vectorizer.py)
if __name__ == "__main__":
    log_path = os.path.join(PROJECT_ROOT, "data", "sample_logs.txt")
    
    logs = read_logs(log_path)
    cleaned = clean_logs(logs)

    vectorizer, vectors = fit_vectorizer(cleaned)

    print("\nTF-IDF shape:", vectors.shape)
    print("Vocabulary size:", len(vectorizer.vocabulary_))
  