import json
from tools import list_input_files, read_file, write_output, log
from ollama_client import generate
from prompts import build_prompt
from rules import apply_rules
from validators import validate_result

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    if text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text

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

        # counts
        category_counts[category] = category_counts.get(category, 0) + 1
        action_counts[final_action] = action_counts.get(final_action, 0) + 1
        queue_counts[queue] = queue_counts.get(queue, 0) + 1

        # high priority
        if priority == "high":
            high_priority.append(f"- {filename}: {item.get('summary', '')}")

        # needs review
        if status == "needs_review":
            needs_review.append(f"- {filename}")

        # processed files
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

def run_agent():
    files = list_input_files()

    if not files:
        log("No input files found.")
        print("No input files found.")
        return

    all_results = []

    for filename in files:
        try:
            email_text = read_file(filename)
            prompt = build_prompt(email_text)
            response_text =  generate(prompt)

            cleaned_response = clean_json_response(response_text)

            try:
                parsed = json.loads(cleaned_response)
            except json.JSONDecodeError:
                parsed = {
                    "category": "general",
                    "priority": "medium",
                    "confidence": 0.0,
                    "reasoning": "invalid json",
                    "summary": "invalid json",
                    "draft_reply": response_text,
                }

                normalized = normalize_result(parsed, filename)
                normalized["parse_error"] = True
                normalized["validation_errors"] = []

                decision = {
                    "final_action": "review_now",
                    "queue": "manual_review",
                    "requires_human": True,
                    "status": "needs_review",
                }

                final_result = {**normalized, **decision}

                output_name = f"{filename}.json"
                write_output(
                    output_name,
                    json.dumps(final_result, indent=2, ensure_ascii=False) + "\n"
                )

                all_results.append(final_result)

                log(f"[PARSE_FAIL] {filename} -> {output_name}")
                print(f"Processed {filename} with parse failure")
                continue

            normalized = normalize_result(parsed, filename)
            normalized["category"] = "weird_category"   # <-- BURAYA
            normalized["parse_error"] = False

            validation = validate_result(normalized)

            if not validation["is_valid"]:
                normalized["validation_errors"] = validation["errors"]

                decision = {
                    "final_action": "review_now",
                    "queue": "manual_review",
                    "requires_human": True,
                    "status": "needs_review",
                }

                log(f"[VALIDATION_FAIL] {filename} -> {validation['errors']}")
            else:
                normalized["validation_errors"] = []
                decision = apply_rules(normalized)

            final_result = {**normalized, **decision}

            output_name = f"{filename}.json"
            write_output(
                output_name,
                json.dumps(final_result, indent=2, ensure_ascii=False) + "\n"
            )

            all_results.append(final_result)

            log(f"[SUCCESS] {filename} -> {output_name}")
            print(f"Processed {filename}")

        except Exception as e:
            log(f"Error processing {filename}: {str(e)}")
            print(f"Error processing {filename}: {str(e)}")

    summary = build_summary_report(all_results)
    write_output("summary.md", summary)
    log("Generated summary.md")
    print("Generated summary.md")