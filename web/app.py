from flask import Flask, render_template, request
import os, sys, joblib

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))
sys.path.append(ROOT)

from src.preprocessing.cleaner import clean_logs

app = Flask(__name__)

model = joblib.load(os.path.join(ROOT, "model.pkl"))
vectorizer = joblib.load(os.path.join(ROOT, "vectorizer.pkl"))


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    pasted_text = ""

    if request.method == "POST":

        pasted_text = request.form.get("paste_logs", "").strip()

        # Use pasted logs first
        if pasted_text:
            raw = [ln for ln in pasted_text.splitlines() if ln.strip()]
        else:
            file = request.files.get("logfile")
            if not file or file.filename == "":
                return render_template("index.html", result=None, pasted=pasted_text)

            content = file.read().decode("utf-8", errors="ignore")
            raw = [ln for ln in content.splitlines() if ln.strip()]

        cleaned = clean_logs(raw)
        vec = vectorizer.transform(cleaned)
        preds = model.predict(vec)

        result = list(zip(raw, preds))

    return render_template("index.html", result=result, pasted=pasted_text)


if __name__ == "__main__":
    app.run(debug=True)
