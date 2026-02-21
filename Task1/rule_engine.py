THRESHOLD = 50

def apply_rules(chunk):

    # ✅ Empty chunk safety
    if not chunk:
        return {"words": 0, "status": "EMPTY"}

    # Convert chunk list into single text
    text = " ".join(chunk)

    # Count words
    word_count = len(text.split())

    # Apply rule
    if word_count > THRESHOLD:
        status = "LARGE"
    else:
        status = "SMALL"

    return {"words": word_count, "status": status}