import os
import sys
from flask import Flask, render_template, request
import joblib

# -------------------------------------------------------
# ABSOLUTE PATH FIX (100% reliable everywhere)
# -------------------------------------------------------
# Path of: Error-Log-Classifier/web/app.py
CURRENT_FILE = os.path.abspath(__file__)

# Move one level up → Error-Log-Classifier/
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

# Allow imports like src.preprocessing.cleaner
sys.path.insert(0, PROJECT_ROOT)

# Model paths
MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")
VEC_PATH = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

# -------------------------------------------------------
# LOAD MODEL + VECTORIZER
# -------------------------------------------------------
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

# Import AFTER fixing sys.path
from src.preprocessing.cleaner import clean_logs
from src.model.predict import predict_log


# -------------------------------------------------------
# FLASK APP
# -------------------------------------------------------
app = Flask(
    __name__, 
    static_folder="static", 
    template_folder="templates"
)


# -------------------------------------------------------
# ROUTE — MAIN PAGE
# -------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    pasted = ""

    if request.method == "POST":
        # ------------------------------
        # 1. Get pasted logs
        # ------------------------------
        pasted = request.form.get("paste_logs", "").strip()

        # ------------------------------
        # 2. Get uploaded file
        # ------------------------------
        file = request.files.get("logfile")

        if file and file.filename:  
            pasted = file.read().decode("utf-8")

        # ------------------------------
        # 3. Classify logs (only if input exists)
        # ------------------------------
        if pasted:
            raw_lines = [line for line in pasted.split("\n") if line.strip()]

            cleaned = clean_logs(raw_lines)
            vectors = vectorizer.transform(cleaned)
            predictions = model.predict(vectors)

            result = list(zip(raw_lines, predictions))

    return render_template("index.html", result=result, pasted=pasted)


# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
