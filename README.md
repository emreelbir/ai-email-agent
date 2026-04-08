# AI Email Triage Agent

A local AI-powered email triage system that classifies emails, assigns priority, and determines actions using a lightweight rule-based decision layer.

## Features

- Local LLM (Ollama)
- Email classification (sales, support, spam, urgent, general)
- Priority detection
- Confidence and reasoning output
- Rule-based decision system
- Batch processing
- Summary report generation

## Architecture

email → LLM → normalize → rules → output

## Example

```json
{
  "category": "support",
  "priority": "high",
  "final_action": "review_now"
}
