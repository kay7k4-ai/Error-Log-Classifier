import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

sample_logs = [
    "INFO: System started successfully",
    "WARNING: Disk usage above 90%",
    "ERROR: Could not connect to database",
    "CRITICAL: Kernel panic detected",
]

X = vectorizer.transform(sample_logs)
pred = model.predict(X)

print(pred)
