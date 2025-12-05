def rule_classify(line: str):
    """
    Simple fallback: look for keywords in raw or cleaned line.
    """
    s = line.lower()
    if "critical" in s:
        return "CRITICAL"
    if "error" in s:
        return "ERROR"
    if "warning" in s:
        return "WARNING"
    if "info" in s:
        return "INFO"
    return "UNKNOWN"
