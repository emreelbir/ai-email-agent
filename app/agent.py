import json

from app.utils.file_ops import list_input_files, read_file, write_output
from app.utils.logger import log

from app.services.llm_client import generate

from app.core.parser import parse_llm_response
from app.core.normalizer import normalize_result
from app.core.validator import validate_result
from app.core.rules import apply_rules
from app.core.summary import build_summary_report

from app.prompts import build_prompt


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

            response_text = generate(prompt)

            parsed, parse_error = parse_llm_response(response_text)

            # ❌ PARSE FAIL
            if parse_error:
                normalized = normalize_result({
                    "summary": "invalid json",
                    "draft_reply": response_text,
                    "reasoning": "invalid json",
                    "confidence": 0.0,
                }, filename)

                normalized["parse_error"] = True
                normalized["validation_errors"] = []

                decision = {
                    "final_action": "review_now",
                    "queue": "manual_review",
                    "requires_human": True,
                    "status": "needs_review",
                }

                log(f"[PARSE_FAIL] {filename}")

            # ✅ NORMAL FLOW
            else:
                normalized = normalize_result(parsed, filename)
                normalized["parse_error"] = False

                validation = validate_result(normalized)

                # ❌ VALIDATION FAIL
                if not validation["is_valid"]:
                    normalized["validation_errors"] = validation["errors"]

                    decision = {
                        "final_action": "review_now",
                        "queue": "manual_review",
                        "requires_human": True,
                        "status": "needs_review",
                    }

                    log(f"[VALIDATION_FAIL] {filename} -> {validation['errors']}")

                # ✅ SUCCESS
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
            log(f"[ERROR] {filename}: {str(e)}")
            print(f"Error processing {filename}: {str(e)}")

    # 📊 SUMMARY
    summary = build_summary_report(all_results)
    write_output("summary.md", summary)

    log("Generated summary.md")
    print("Generated summary.md")