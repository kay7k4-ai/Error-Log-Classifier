import re
import os
import sys

# FIX IMPORT PATHS AUTOMATICALLY

# Get project root directory (two levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

# Now import works from ANY location
from src.preprocessor import read_logs

# SIMPLE CLEANING FUNCTIONS (NO NLTK)

stop_words = {
    "the","and","is","to","for","in","on","at","a","an","of","this","that","it",
    "with","as","by","be","from","or","are","was","were"
}

def clean_line(line):
    """Cleans a single log line."""
    # Remove timestamp
    line = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "", line)

    # Lowercase
    line = line.lower()

    # Remove paths like /api/data
    line = re.sub(r"/\S+", "", line)

    # Remove numbers
    line = re.sub(r"\d+", "", line)

    # Remove special characters
    line = re.sub(r"[^a-zA-Z\s]", " ", line)

    # Tokenize
    words = line.split()

    # Remove stopwords
    filtered = [w for w in words if w not in stop_words]

    return " ".join(filtered)


def clean_logs(log_list):
    """Cleans every log line."""
    return [clean_line(line) for line in log_list]

# RUN DIRECTLY FOR TESTING
if __name__ == "__main__":

    # ALWAYS use full path to your sample logs
    log_path = os.path.join(PROJECT_ROOT, "data", "sample_logs.txt")

    logs = read_logs(log_path)

    print("\nRAW LOGS:")
    for l in logs:
        print(l.strip())

    cleaned = clean_logs(logs)

    print("\nCLEANED LOGS:")
    for c in cleaned:
        print(c)
