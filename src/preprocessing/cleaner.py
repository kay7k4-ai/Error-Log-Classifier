import re

_stop_words = {
    "the","and","is","to","for","in","on","at","a","an","of","this","that","it",
    "with","as","by","be","from","or","are","was","were","i","you","we","they"
}

def clean_line(line: str) -> str:
    """
    Clean a single log line but keep category words (error, warning, info, critical).
    """
    if not isinstance(line, str):
        return ""

    line = line.lower()

    # Remove common timestamp patterns: 2024-07-19 12:22:10 or 2024-07-19T12:22:10
    line = re.sub(r"\d{4}-\d{2}-\d{2}[ t]\d{2}:\d{2}:\d{2}", " ", line)

    # Remove ip addresses and numbers but keep words
    line = re.sub(r"\d+\.\d+\.\d+\.\d+", " ", line)
    line = re.sub(r"\d+", " ", line)

    # Remove file paths
    line = re.sub(r"/\S+", " ", line)

    # Keep letters and spaces only
    line = re.sub(r"[^a-z\s]", " ", line)

    tokens = [t for t in line.split() if t and t not in _stop_words]

    return " ".join(tokens)

def clean_logs(logs):
    return [clean_line(l) for l in logs]
