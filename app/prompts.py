def build_prompt(email_text):
    return f"""
You are an AI email triage assistant.

Analyze the email and return ONLY valid JSON.

Use this format:
{{
  "category": "sales | support | spam | urgent | general",
  "priority": "low | medium | high",
  "confidence": 0.0,
  "reasoning": "short explanation why you classified it this way",
  "summary": "short summary",
  "draft_reply": "short professional reply"
}}

Rules:
- confidence must be between 0 and 1
- reasoning must be concise
- no markdown, no code blocks, ONLY JSON

Email:
\"\"\"
{email_text}
\"\"\"
"""
