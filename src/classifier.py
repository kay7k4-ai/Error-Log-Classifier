def classify_log_line(line):
    line = line.lower()
    if "critical" in line:
        return "CRITICAL"
    if "error" in line:
        return "ERROR"
    if "warning" in line:
        return "WARNING"
    if "info" in line:
        return "INFO"
    return "UNKNOWN"
