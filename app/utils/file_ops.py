import os

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