VALID_CATEGORIES = {"sales", "support", "spam", "urgent", "general"}
VALID_PRIORITIES = {"low", "medium", "high"}

def validate_result(result: dict) -> dict:
    errors = []

    category = result.get("category")
    priority = result.get("priority")
    confidence = result.get("confidence")
    summary = result.get("summary")
    draft_reply = result.get("draft_reply")

    if category not in VALID_CATEGORIES:
        errors.append(f"invalid category: {category}")

    if priority not in VALID_PRIORITIES:
        errors.append(f"invalid priority: {priority}")

    try:
        confidence = float(confidence)
        if confidence < 0 or confidence > 1:
            errors.append(f"confidence out of range: {confidence}")
    except (TypeError, ValueError):
        errors.append(f"invalid confidence: {confidence}")

    if not summary or not str(summary).strip():
        errors.append("missing summary")

    if not draft_reply or not str(draft_reply).strip():
        errors.append("missing draft_reply")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }