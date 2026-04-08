import os
from datetime import datetime

WORKSPACE = "/workspace"

def list_input_files():
    input_dir = os.path.join(WORKSPACE, "input")
    if not os.path.exists(input_dir):
        return []
    return [f for f in os.listdir(input_dir) if f.endswith(".txt") or f.endswith(".md")]

def read_file(filename):
    path = os.path.join(WORKSPACE, "input", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_output(filename, content):
    path = os.path.join(WORKSPACE, "output", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def log(message):
    path = os.path.join(WORKSPACE, "logs", "agent.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")
        
def normalize_result(result: dict, filename: str) -> dict:
    return {
        "filename": filename,
        "category": result.get("category", "general"),
        "priority": result.get("priority", "low"),
        "confidence": result.get("confidence", 0.0),
        "reasoning": result.get("reasoning", ""),
        "summary": result.get("summary", ""),
        "draft_reply": result.get("draft_reply", ""),
    }