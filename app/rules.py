def apply_rules(result: dict) -> dict:
    category = result.get("category", "general")
    priority = result.get("priority", "low")
    confidence = result.get("confidence", 0)

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    final_action = "queue"
    queue = category
    requires_human = False
    status = "ready"

    if confidence < 0.60:
        final_action = "review_now"
        queue = "manual_review"
        requires_human = True
        status = "needs_review"

    elif category == "spam":
        final_action = "ignore"
        queue = "spam"

    elif category == "urgent":
        final_action = "escalate"
        queue = "urgent"
        requires_human = True

    elif priority == "high":
        final_action = "review_now"
        queue = category
        requires_human = True

    return {
        "final_action": final_action,
        "queue": queue,
        "requires_human": requires_human,
        "status": status,
    }
