import os

def read_logs(file_path):
    """
    Read a log file into a list of lines.
    Returns [] if file not found or empty.
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    return lines
