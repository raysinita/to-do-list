import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE.name} is corrupted. Starting fresh.")
        return []


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, indent=2))


def show_tasks(tasks: list[dict]) -> None:
    if not tasks:
        print("\n  (no tasks yet — add one with option 1)\n")
        return
    print()
    for i, t in enumerate(tasks, 1):
        mark = "[x]" if t["done"] else "[ ]"
        print(f"  {i:>2}. {mark} {t['title']}")
    print()


def prompt_index(tasks: list[dict], action: str) -> int | None:
    if not tasks:
        print("No tasks to " + action + ".")
        return None
    raw = input(f"Task number to {action}: ").strip()
    if not raw.isdigit():
        print("Please enter a number.")
        return None
    idx = int(raw) - 1
    if not 0 <= idx < len(tasks):
        print("That task number doesn't exist.")
        return None
    return idx


def add_task(tasks: list[dict]) -> None:
    title = input("New task: ").strip()
    if not title:
        print("Task title can't be empty.")
        return
    tasks.append({
        "title": title,
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    })
    print(f"Added: {title}")


def toggle_task(tasks: list[dict]) -> None:
    idx = prompt_index(tasks, "toggle")
    if idx is None:
        return
    tasks[idx]["done"] = not tasks[idx]["done"]
    state = "done" if tasks[idx]["done"] else "not done"
    print(f"Marked '{tasks[idx]['title']}' as {state}.")


def delete_task(tasks: list[dict]) -> None:
    idx = prompt_index(tasks, "delete")
    if idx is None:
        return
    removed = tasks.pop(idx)
    print(f"Deleted: {removed['title']}")


def clear_done(tasks: list[dict]) -> None:
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    print(f"Cleared {before - len(tasks)} completed task(s).")


MENU = """
What would you like to do?
  1. Add task
  2. Toggle done/undone
  3. Delete task
  4. Clear all completed
  5. Quit
"""


def main() -> None:
    tasks = load_tasks()
    print("=" * 40)
    print(" To-do list")
    print("=" * 40)

    actions = {
        "1": add_task,
        "2": toggle_task,
        "3": delete_task,
        "4": clear_done,
    }

    while True:
        show_tasks(tasks)
        print(MENU)
        choice = input("Choice [1-5]: ").strip()
        if choice == "5" or choice.lower() in {"q", "quit", "exit"}:
            save_tasks(tasks)
            print("Saved. Bye!")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid choice — pick 1-5.")
            continue
        action(tasks)
        save_tasks(tasks)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted. Changes saved up to last action.")
