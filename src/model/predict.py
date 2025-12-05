import os, joblib
from src.preprocessing.cleaner import clean_logs
from src.classifier import rule_classify

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")
VEC_PATH = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

# Lazy loader
_model = None
_vectorizer = None
def _ensure():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VEC_PATH)
    return _model, _vectorizer

def predict_log(log_text):
    """
    Predict category for a single log line.
    Uses model + fallback rule-based classifier.
    """
    model, vectorizer = _ensure()
    cleaned = clean_logs([log_text])
    vec = vectorizer.transform(cleaned)
    pred = model.predict(vec)[0]
    # If model produces something odd, fallback
    if pred is None or pred == "" or pred == "UNKNOWN":
        return rule_classify(log_text)
    return pred

def predict_batch(raw_logs, vectorizer_obj=None, model_obj=None):
    """
    Predict batch of raw logs. If model_obj/vectorizer_obj passed, use them.
    Returns list of tuples (raw_line, category)
    """
    model_local = model_obj
    vectorizer_local = vectorizer_obj
    if model_local is None or vectorizer_local is None:
        model_local, vectorizer_local = _ensure()
    cleaned = clean_logs(raw_logs)
    vectors = vectorizer_local.transform(cleaned)
    preds = model_local.predict(vectors)
    # apply fallback per line if needed
    out = []
    for raw, p in zip(raw_logs, preds):
        if not p or p == "UNKNOWN":
            p = rule_classify(raw)
        out.append((raw, p))
    return out
