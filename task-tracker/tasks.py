#!/usr/bin/env python3
import sqlite3
import sys
from datetime import datetime

DB = "tasks.db"

def connect():
    return sqlite3.connect(DB)

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def add_task(conn):
    title = input("Title: ").strip()
    if not title:
        print("Title is required.")
        return
    priority = input("Priority (low/medium/high, default medium): ").strip().lower()
    if priority not in ("low", "medium", "high"):
        priority = "medium"
    due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
    conn.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (title, priority, due_date if due_date else None)
    )
    conn.commit()
    print(f"Task '{title}' added.")

def list_tasks(conn):
    tasks = conn.execute(
        "SELECT id, title, priority, due_date, status FROM tasks ORDER BY created_at DESC"
    ).fetchall()
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<5} {'Title':<25} {'Priority':<10} {'Due':<12} {'Status'}")
    print("-" * 65)
    for t in tasks:
        tid, title, priority, due, status = t
        due_display = due if due else "-"
        print(f"{tid:<5} {title[:24]:<25} {priority:<10} {due_display:<12} {status}")

def mark_done(conn):
    list_tasks(conn)
    tid = input("Enter task ID to mark done: ").strip()
    if not tid.isdigit():
        print("Invalid ID.")
        return
    conn.execute("UPDATE tasks SET status='done' WHERE id=?", (tid,))
    if conn.total_changes == 0:
        print("No task with that ID.")
    else:
        conn.commit()
        print("Task marked as done.")

def delete_task(conn):
    list_tasks(conn)
    tid = input("Enter task ID to delete: ").strip()
    if not tid.isdigit():
        print("Invalid ID.")
        return
    conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
    if conn.total_changes == 0:
        print("No task with that ID.")
    else:
        conn.commit()
        print("Task deleted.")

def main():
    conn = connect()
    init_db(conn)
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            list_tasks(conn)
        elif cmd == "done" and len(sys.argv) == 3:
            tid = sys.argv[2]
            if tid.isdigit():
                conn.execute("UPDATE tasks SET status='done' WHERE id=?", (tid,))
                conn.commit()
                print("Task marked done.")
            else:
                print("Invalid ID.")
        elif cmd == "delete" and len(sys.argv) == 3:
            tid = sys.argv[2]
            if tid.isdigit():
                conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
                conn.commit()
                print("Task deleted.")
            else:
                print("Invalid ID.")
        else:
            print("Usage: python tasks.py [add|list|done ID|delete ID]")
    else:
        while True:
            print("\n1. Add Task")
            print("2. List Tasks")
            print("3. Mark Task Done")
            print("4. Delete Task")
            print("5. Exit")
            choice = input("> ").strip()
            if choice == "1":
                add_task(conn)
            elif choice == "2":
                list_tasks(conn)
            elif choice == "3":
                mark_done(conn)
            elif choice == "4":
                delete_task(conn)
            elif choice == "5":
                break
            else:
                print("Invalid option.")
    conn.close()

if __name__ == "__main__":
    main()
