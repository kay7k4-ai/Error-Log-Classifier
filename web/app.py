import os
import sys
from flask import Flask, render_template, request
import joblib

# PATH FIX
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.preprocessing.cleaner import clean_logs
from src.model.predict import predict_log

app = Flask(__name__)

# Load model and vectorizer
MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")
VEC_PATH = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)


@app.route("/", methods=["GET", "POST"])
def index():

    pasted = ""
    result = None

    if request.method == "POST":

        pasted = request.form.get("paste_logs", "").strip()
        file = request.files.get("logfile")

        raw_logs = []

        # 1️⃣ If user pasted logs → PRIORITY
        if pasted:
            raw_logs = pasted.splitlines()

        # 2️⃣ If file is uploaded → use it
        elif file and file.filename:
            raw_logs = file.read().decode("utf-8").splitlines()

        # 3️⃣ If nothing given → return empty
        if not raw_logs:
            return render_template("index.html", result=None, pasted=pasted)

        # Clean, vectorize, predict
        cleaned = clean_logs(raw_logs)
        vectors = vectorizer.transform(cleaned)
        predictions = model.predict(vectors)

        result = list(zip(raw_logs, predictions))

    return render_template("index.html", result=result, pasted=pasted)


if __name__ == "__main__":
    app.run(debug=True)
