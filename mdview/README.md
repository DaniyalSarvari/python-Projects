markdown
# mdview - Markdown Live Preview

Instantly preview any Markdown file in your browser with automatic reload on save.

## Features

- Converts Markdown to clean HTML
- Serves locally at `http://localhost:8080`
- Auto-refreshes when the source file changes
- No dependencies beyond Python standard library + `markdown`
- Beautiful default styling

## Installation

```bash
pip install markdown
```
## Usage
```bash
python mdview.py README.md
```
# Or specify a port
```text
python mdview.py notes.md 9090
```
Open your browser manually or let it auto-open. Edit the file — the page updates live.

# How it works
- Reads the Markdown file and converts to HTML.

- Starts a lightweight HTTP server on localhost.

- A background thread watches the file's modification time every second.

- The HTML page includes a JavaScript polling script that checks Last-Modified headers and reloads.

# File structure
```text
mdview/
├── mdview.py
└── README.md
```
# License
MIT
