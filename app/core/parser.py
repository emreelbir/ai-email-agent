import json

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    if text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


def parse_llm_response(response_text):
    cleaned = clean_json_response(response_text)

    try:
        return json.loads(cleaned), False
    except json.JSONDecodeError:
        return None, True