# Task Tracker

A fast, keyboard-driven task manager that lives in your terminal. No mouse, no nonsense. Built with Python and SQLite — your data stays local forever.

## Why this exists

I wanted a todo list that:
- launches in under 0.1 seconds
- doesn't require an internet connection
- lets me add / list / finish / delete tasks without taking my hands off the keyboard
- stores everything in a single file I can back up easily

## What it does

- Add tasks with a **priority** (low / medium / high) and an optional **due date**
- View all tasks in a clean table with colors (coming soon)
- Mark tasks as done
- Delete tasks
- Pipe-friendly CLI mode for scripting (`python tasks.py list`, `python tasks.py done 3`)

## Quick start

```bash
# First run – creates tasks.db automatically
python tasks.py

# Or jump straight to commands:
python tasks.py list
python tasks.py done 2
python tasks.py delete 4


## Example session

$ python tasks.py

1. Add Task
2. List Tasks
3. Mark Task Done
4. Delete Task
5. Exit
> 1

Title: Buy groceries
Priority (low/medium/high): high
Due date (YYYY-MM-DD): 2025-06-02
Task 'Buy groceries' added.

> 2
ID    Title                     Priority   Due          Status
-----------------------------------------------------------------
1     Buy groceries             high       2025-06-02   pending
```

## File structure
```bash
task-tracker/
├── tasks.py      ← the whole application (single file)
├── tasks.db      ← SQLite database (auto-created, not committed)
└── README.md
```

## Why SQLite?
It's embedded, serverless, and rock-solid. No config, no connection strings. Just a file.

## License
MIT — use it however you want.
