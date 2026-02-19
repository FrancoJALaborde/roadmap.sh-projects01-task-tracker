import os
import json
from datetime import datetime
from typing import List, Dict, Optional

TASKS_FILE: str = 'tasks.json'

# ANSI codes for Matrix style xD
MATRIX_GREEN = '\033[92m'
MATRIX_BOLD = '\033[1m'
MATRIX_RESET = '\033[0m'
MATRIX_BG = '\033[40m'

def matrix_print(text: str) -> None:
    print(f"{MATRIX_BG}{MATRIX_GREEN}{MATRIX_BOLD}{text}{MATRIX_RESET}")

def load_tasks() -> List[Dict]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks: List[Dict]) -> None:
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def generate_id(tasks: List[Dict]) -> int:
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def find_task(tasks: List[Dict], task_id: int) -> Optional[Dict]:
    return next((task for task in tasks if task['id'] == task_id), None)

def add_task(description: str) -> Dict:
    tasks = load_tasks()
    now = datetime.now().isoformat()
    task = {
        'id': generate_id(tasks),
        'description': description,
        'status': 'to-do',
        'createdAt': now,
        'updatedAt': now
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

def update_task(task_id: int, new_description: str) -> bool:
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        return False
    task['description'] = new_description
    task['updatedAt'] = datetime.now().isoformat()
    save_tasks(tasks)
    return True

def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    initial_len = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) == initial_len:
        return False
    save_tasks(tasks)
    return True

def mark_task_status(task_id: int, status: str) -> bool:
    if status not in ('to-do', 'in-progress', 'done'):
        return False
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        return False
    task['status'] = status
    task['updatedAt'] = datetime.now().isoformat()
    save_tasks(tasks)
    return True

def list_tasks(status: Optional[str] = None) -> List[Dict]:
    tasks = load_tasks()
    if status:
        if status not in ('to-do', 'in-progress', 'done'):
            return []
        return [task for task in tasks if task['status'] == status]
    return tasks

def print_task(task: Dict) -> None:
    matrix_print(f"ID: {task['id']}")
    matrix_print(f"Description: {task['description']}")
    matrix_print(f"Status: {task['status']}")
    matrix_print(f"Created: {task['createdAt']}")
    matrix_print(f"Update: {task['updatedAt']}")
    matrix_print("-" * 30)

def print_tasks(tasks: List[Dict]) -> None:
    if not tasks:
        matrix_print("There are no tasks to show.")
        return
    for task in tasks:
        print_task(task)

def show_help() -> None:
    help_text = """
Available commands:
  add <description>                Add a new task
  update <ID> <new description>    Update the description of a task
  delete <ID>                      Delete a task
  mark-in-progress <ID>            Mark a task as 'in-progress'
  mark-done <ID>                   Mark a task as 'done'
  list                             List all tasks
  list done                        List all "done" tasks
  list to-do                       List all "to do" tasks
  list in-progress                 List all "in progress" tasks
  help                             Show this help
  exit                             Exit
"""
    matrix_print(help_text)

def main() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    matrix_print("Welcome to the Task Tracker CLI [Matrix Style] (o_-)")
    show_help()
    while True:
        try:
            user_input = input(f"{MATRIX_BG}{MATRIX_GREEN}{MATRIX_BOLD}> {MATRIX_RESET}").strip()
            if not user_input:
                continue
            args = user_input.split()
            command = args[0]

            if command == "add":
                if len(args) < 2:
                    matrix_print("Error: You must provide a description.")
                    continue
                description = " ".join(args[1:])
                task = add_task(description)
                matrix_print(f"Task added successfully (ID: {task['id']})")

            elif command == "update":
                if len(args) < 3:
                    matrix_print("Error: You must provide the ID and new description.")
                    continue
                try:
                    task_id = int(args[1])
                except ValueError:
                    matrix_print("Error: ID must be a number.")
                    continue
                new_description = " ".join(args[2:])
                if update_task(task_id, new_description):
                    matrix_print("Task updated successfully.")
                else:
                    matrix_print("Error: Task not found.")

            elif command == "delete":
                if len(args) < 2:
                    matrix_print("Error: You must provide the task ID.")
                    continue
                try:
                    task_id = int(args[1])
                except ValueError:
                    matrix_print("Error: ID must be a number.")
                    continue
                if delete_task(task_id):
                    matrix_print("Task successfully deleted.")
                else:
                    matrix_print("Error: Task not found.")

            elif command == "mark-in-progress":
                if len(args) < 2:
                    matrix_print("Error: You must provide the task ID.")
                    continue
                try:
                    task_id = int(args[1])
                except ValueError:
                    matrix_print("Error: ID must be a number.")
                    continue
                if mark_task_status(task_id, "in-progress"):
                    matrix_print("Task marked 'in-progress'.")
                else:
                    matrix_print("Error: Task not found.")

            elif command == "mark-done":
                if len(args) < 2:
                    matrix_print("Error: You must provide the task ID.")
                    continue
                try:
                    task_id = int(args[1])
                except ValueError:
                    matrix_print("Error: ID must be a number.")
                    continue
                if mark_task_status(task_id, "done"):
                    matrix_print("Task marked 'done'.")
                else:
                    matrix_print("Error: Task not found.")

            elif command == "list":
                status = None
                if len(args) == 2:
                    status = args[1]
                tasks = list_tasks(status)
                print_tasks(tasks)

            elif command in ("help", "--help", "-h"):
                show_help()

            elif command == "exit":
                matrix_print("Goodbye, Mr. Anderson")
                break

            else:
                matrix_print(f"Unknown command: {command}")
                show_help()

        except Exception as e:
            matrix_print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()