"""Serve verified, actual program executions for browser screenshots.

Run from Homework3: python3 -B tests/record_runs.py
This viewer uses only the Python standard library and writes no result files.
"""

import argparse
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"
SCRIPTS = {
    "p1": "palindrome.py", "p2": "substrings.py",
    "p3": "stacks.py", "p4": "ghostbusters.py",
}


def normalized(data):
    """Normalize only CRLF so all other output bytes remain significant."""
    return data.replace(b"\r\n", b"\n")


def capture(run_id, title, arguments, input_bytes=None, input_path=None,
            expected_path=None):
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-B", *arguments], input=input_bytes or b"",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT,
        env=environment, timeout=60,
    )
    if result.returncode:
        raise RuntimeError(f"{run_id} exited with status {result.returncode}:\n"
                           + result.stderr.decode("utf-8", errors="replace"))
    if expected_path is not None:
        if result.stderr:
            raise RuntimeError(f"{run_id} produced unexpected standard error")
        if normalized(result.stdout) != normalized(expected_path.read_bytes()):
            raise RuntimeError(f"{run_id} does not match {expected_path.name}")
    command = "python3 -B " + " ".join(arguments)
    if input_path is not None:
        command += " < " + input_path.relative_to(ROOT).as_posix()
    return {
        "id": run_id, "filename": run_id + ".jpg", "title": title,
        "path": "/run/" + run_id, "command": command,
        "input": None if input_bytes is None else normalized(input_bytes).decode("utf-8"),
        "stdout": normalized(result.stdout).decode("utf-8"),
        "stderr": normalized(result.stderr).decode("utf-8"),
        "status": result.returncode, "verified": expected_path is not None,
    }


def collect_runs():
    records = []
    inputs = sorted(DATA.glob("*_input.txt"))
    if not inputs:
        raise RuntimeError("No input fixtures found")
    for input_path in inputs:
        run_id = input_path.name.removesuffix("_input.txt")
        prefix, label = run_id.split("_", 1)
        script = SCRIPTS[prefix]
        expected_path = input_path.with_name(run_id + "_expected.txt")
        records.append(capture(
            run_id, "Problem " + prefix[1:] + " — " + label.replace("_", " "),
            [script], input_path.read_bytes(), input_path, expected_path,
        ))
    records.append(capture(
        "p3_stacks", "Problem 3 — three stack implementations", ["stacks.py"],
        expected_path=DATA / "p3_expected.txt",
    ))
    records.sort(key=lambda record: record["id"])
    records.append(capture(
        "tests_unittest", "Automated tests",
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
    ))
    return records


STYLE = """
body { margin: 0 auto; max-width: 1200px; padding: 32px 40px;
       color: #17202b; background: #fff; font: 16px/1.5 Arial, sans-serif; }
h1 { margin: 0 0 6px; font-size: 28px; }
h2 { margin: 23px 0 8px; font-size: 17px; }
.meta { color: #4d5968; font-size: 14px; }
pre { margin: 0; padding: 15px 18px; border: 1px solid #d3d9e1;
      background: #f7f9fc; font: 14px/1.55 Consolas, monospace;
      white-space: pre-wrap; overflow-wrap: anywhere; min-height: 22px; }
.status { margin-top: 24px; border-top: 1px solid #d3d9e1; padding-top: 12px; }
a { color: #215aaa; } li { margin: 8px 0; }
"""


def document(title, body):
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<title>" + html.escape(title) + "</title><style>" + STYLE
            + "</style></head><body>" + body + "</body></html>")


def run_page(record):
    body = "<h1>" + html.escape(record["title"]) + "</h1>"
    body += ("<div class='meta'>Actual execution viewer · Python "
             + html.escape(platform.python_version()) + "</div>")
    body += "<h2>Command</h2><pre>" + html.escape(record["command"]) + "</pre>"
    if record["input"] is not None:
        label = "Input (empty input)" if record["input"] == "" else "Input"
        body += "<h2>" + label + "</h2><pre>" + html.escape(record["input"]) + "</pre>"
    label = "Actual stdout (empty)" if record["stdout"] == "" else "Actual stdout"
    body += "<h2>" + label + "</h2><pre>" + html.escape(record["stdout"]) + "</pre>"
    if record["stderr"]:
        body += "<h2>Actual stderr</h2><pre>" + html.escape(record["stderr"]) + "</pre>"
    body += "<div class='status'>Exit status: " + str(record["status"])
    if record["verified"]:
        body += " <span class='meta'>· Expected output verified</span>"
    body += "</div>"
    return document(record["title"], body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()
    records = collect_runs()
    if arguments.verify_only:
        print(f"Verified {len(records)} actual executions.")
        return
    lookup = {record["path"]: record for record in records}
    manifest = [{key: record[key] for key in ("id", "filename", "title", "path")}
                for record in records]

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            content_type = "text/html; charset=utf-8"
            if path == "/health":
                payload, content_type = "ready", "text/plain; charset=utf-8"
            elif path == "/manifest":
                payload = json.dumps(manifest, ensure_ascii=False)
                content_type = "application/json; charset=utf-8"
            elif path == "/":
                links = "".join("<li><a href='" + html.escape(record["path"]) + "'>"
                                + html.escape(record["title"]) + "</a></li>"
                                for record in records)
                body = ("<h1>Execution viewer</h1><div class='meta'>Python "
                        + html.escape(platform.python_version())
                        + " · Actual executions: " + str(len(records)) + "</div>"
                        + "<h2>Command</h2><pre>python3 -B tests/record_runs.py</pre>"
                        + "<h2>Captured executions</h2><ul>" + links + "</ul>")
                payload = document("Execution viewer", body)
            elif path in lookup:
                payload = run_page(lookup[path])
            else:
                self.send_error(404)
                return
            encoded = payload.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(encoded)

        def log_message(self, *_):
            pass

    with HTTPServer(("127.0.0.1", arguments.port), Handler) as server:
        print(f"Ready: http://127.0.0.1:{arguments.port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
