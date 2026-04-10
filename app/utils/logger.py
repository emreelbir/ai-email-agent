import os
from datetime import datetime

WORKSPACE = "/workspace"

def log(message):
    path = os.path.join(WORKSPACE, "logs", "agent.log")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")