"""Streamlit to-do list with JSON persistence."""

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, indent=2))


st.set_page_config(page_title="To-do list", page_icon="✅", layout="centered")
st.title("✅ To-do list")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks


def add_task() -> None:
    title = st.session_state.new_task.strip()
    if title:
        tasks.append({
            "title": title,
            "done": False,
            "created": datetime.now().isoformat(timespec="seconds"),
        })
        save_tasks(tasks)
        st.session_state.new_task = ""


st.text_input(
    "New task",
    key="new_task",
    placeholder="What do you need to do?",
    on_change=add_task,
    label_visibility="collapsed",
)

st.divider()

if not tasks:
    st.info("No tasks yet — add one above.")
else:
    for i, task in enumerate(tasks):
        col_check, col_title, col_delete = st.columns([1, 10, 1])

        with col_check:
            new_done = st.checkbox(
                "done",
                value=task["done"],
                key=f"done_{i}_{task['created']}",
                label_visibility="collapsed",
            )
            if new_done != task["done"]:
                task["done"] = new_done
                save_tasks(tasks)
                st.rerun()

        with col_title:
            if task["done"]:
                st.markdown(f"~~{task['title']}~~")
            else:
                st.markdown(task["title"])

        with col_delete:
            if st.button("🗑", key=f"del_{i}_{task['created']}", help="Delete"):
                tasks.pop(i)
                save_tasks(tasks)
                st.rerun()

    st.divider()
    done_count = sum(1 for t in tasks if t["done"])
    total = len(tasks)
    col_stats, col_clear = st.columns([3, 1])
    with col_stats:
        st.caption(f"{done_count} of {total} done")
    with col_clear:
        if done_count and st.button("Clear completed"):
            st.session_state.tasks = [t for t in tasks if not t["done"]]
            save_tasks(st.session_state.tasks)
            st.rerun()
