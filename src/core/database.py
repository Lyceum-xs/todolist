# database.py
import json
import os
from typing import List
from models import Task

# place tasks.json in project root (one level above src)
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(script_dir, 'tasks.json')

def load_tasks() -> List[Task]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Task(**t) for t in data]

def save_tasks(tasks: List[Task]):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([t.__dict__ for t in tasks], f, ensure_ascii=False, indent=2)

def generate_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1