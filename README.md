## How It Works

1. Reads email files from workspace/input
2. Sends content to local LLM (Ollama)
3. Parses and normalizes output
4. Applies deterministic rules
5. Generates structured JSON and summary report

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
