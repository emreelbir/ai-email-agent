def build_summary_report(results):
    total = len(results)

    category_counts = {}
    action_counts = {}
    queue_counts = {}
    high_priority = []
    needs_review = []
    processed_files = []

    for item in results:
        category = item.get("category", "unknown")
        priority = item.get("priority", "unknown")
        filename = item.get("filename", "unknown")
        final_action = item.get("final_action", "unknown")
        queue = item.get("queue", "unknown")
        status = item.get("status", "unknown")

        category_counts[category] = category_counts.get(category, 0) + 1
        action_counts[final_action] = action_counts.get(final_action, 0) + 1
        queue_counts[queue] = queue_counts.get(queue, 0) + 1

        if priority == "high":
            high_priority.append(f"- {filename}: {item.get('summary', '')}")

        if status == "needs_review":
            needs_review.append(f"- {filename}")

        processed_files.append(
            f"- {filename}: {category} / {priority} / {final_action}"
        )

    lines = []
    lines.append("# Inbox Summary")
    lines.append("")
    lines.append(f"Total emails: {total}")
    lines.append("")

    lines.append("## Category Breakdown")
    lines.append("")
    for category, count in sorted(category_counts.items()):
        lines.append(f"- {category}: {count}")
    lines.append("")

    lines.append("## Action Breakdown")
    lines.append("")
    for action, count in sorted(action_counts.items()):
        lines.append(f"- {action}: {count}")
    lines.append("")

    lines.append("## Queue Breakdown")
    lines.append("")
    for queue, count in sorted(queue_counts.items()):
        lines.append(f"- {queue}: {count}")
    lines.append("")

    lines.append("## High Priority")
    lines.append("")
    if high_priority:
        lines.extend(high_priority)
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Needs Review")
    lines.append("")
    if needs_review:
        lines.extend(needs_review)
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Processed Files")
    lines.append("")
    lines.extend(processed_files)

    return "\n".join(lines) + "\n"