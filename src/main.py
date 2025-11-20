from classifier import classify_log_line

file = "../data/sample_logs.txt"

with open(file, "r") as f:
    lines = f.readlines()

result = {"CRITICAL":0,"ERROR":0,"WARNING":0,"INFO":0,"UNKNOWN":0}

for line in lines:
    cat = classify_log_line(line)
    result[cat] += 1

print("\n--- LOG SUMMARY ---")
for k,v in result.items():
    print(f"{k}: {v}")
