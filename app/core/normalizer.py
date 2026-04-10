def normalize_result(result, filename):
    return {
        "filename": filename,
        "category": result.get("category", "general"),
        "priority": result.get("priority", "low"),
        "confidence": result.get("confidence", 0.0),
        "reasoning": result.get("reasoning", ""),
        "summary": result.get("summary", ""),
        "draft_reply": result.get("draft_reply", ""),
    }