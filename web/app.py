import os
import sys
from flask import Flask, render_template, request, jsonify
import joblib

# -------------------------------------------------------
# ABSOLUTE PATH FIX
# -------------------------------------------------------
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))
sys.path.insert(0, PROJECT_ROOT)

MODEL_PATH = os.path.join(PROJECT_ROOT, "model.pkl")
VEC_PATH   = os.path.join(PROJECT_ROOT, "vectorizer.pkl")

# -------------------------------------------------------
# LOAD MODEL + VECTORIZER
# -------------------------------------------------------
model      = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

from src.preprocessing.cleaner import clean_logs

# -------------------------------------------------------
# FLASK APP
# -------------------------------------------------------
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# -------------------------------------------------------
# ROUTE — MAIN PAGE (kept exactly as before)
# -------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    pasted = ""

    if request.method == "POST":
        pasted = request.form.get("paste_logs", "").strip()
        file   = request.files.get("logfile")

        if file and file.filename:
            pasted = file.read().decode("utf-8")

        if pasted:
            raw_lines   = [line for line in pasted.split("\n") if line.strip()]
            cleaned     = clean_logs(raw_lines)
            vectors     = vectorizer.transform(cleaned)
            predictions = model.predict(vectors)
            result      = list(zip(raw_lines, predictions))

    return render_template("index.html", result=result, pasted=pasted)


# -------------------------------------------------------
# ROUTE — /classify  (used by the new JS frontend)
# Accepts:  POST  { "logs": ["line1", "line2", ...] }
# Returns:  { "results": [{ "text": "line1", "type": "ERROR" }, ...] }
# -------------------------------------------------------
@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json(silent=True)

    if not data or "logs" not in data:
        return jsonify({"error": "Send JSON body: {\"logs\": [\"line1\", \"line2\", ...]}"}), 400

    raw_lines = [str(line) for line in data["logs"] if str(line).strip()]

    if not raw_lines:
        return jsonify({"results": []}), 200

    cleaned     = clean_logs(raw_lines)
    vectors     = vectorizer.transform(cleaned)
    predictions = model.predict(vectors)

    results = [
        {"text": raw, "type": str(pred)}
        for raw, pred in zip(raw_lines, predictions)
    ]

    return jsonify({"results": results}), 200


# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)