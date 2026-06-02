#!/usr/bin/env python3
import sys
import time
import threading
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import markdown

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }}
pre {{ background: #f4f4f4; padding: 1rem; overflow-x: auto; }}
code {{ background: #f4f4f4; padding: 0.2em 0.4em; border-radius: 3px; }}
</style>
<script>
let lastModified = null;
setInterval(() => {{
    fetch(window.location.href, {{ method: 'HEAD' }})
        .then(r => {{
            const modified = r.headers.get('Last-Modified');
            if (lastModified && lastModified !== modified) location.reload();
            lastModified = modified;
        }});
}}, 1000);
</script>
</head>
<body>{body}</body>
</html>
"""

class MarkdownHandler(SimpleHTTPRequestHandler):
    md_file = None
    html_content = ""

    @classmethod
    def set_md_file(cls, path):
        cls.md_file = path
        cls.update_html()

    @classmethod
    def update_html(cls):
        with open(cls.md_file, "r", encoding="utf-8") as f:
            md_text = f.read()
        body = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
        cls.html_content = TEMPLATE.format(
            title=Path(cls.md_file).stem,
            body=body
        )

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.html_content.encode("utf-8"))
        else:
            super().do_GET()

def watcher(md_path):
    last_mtime = md_path.stat().st_mtime
    while True:
        time.sleep(1)
        try:
            current_mtime = md_path.stat().st_mtime
            if current_mtime != last_mtime:
                MarkdownHandler.update_html()
                last_mtime = current_mtime
        except FileNotFoundError:
            pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python mdview.py <markdown_file> [port]")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)

    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

    MarkdownHandler.set_md_file(md_path)

    # Start file watcher in background
    t = threading.Thread(target=watcher, args=(md_path,), daemon=True)
    t.start()

    server = HTTPServer(("localhost", port), MarkdownHandler)
    url = f"http://localhost:{port}"
    print(f"Serving {md_path.name} at {url}")
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()

if __name__ == "__main__":
    main()
