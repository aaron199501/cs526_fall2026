"""Serve verified, actual program executions for browser screenshots.

Run from Homework3: python3 -B tests/record_runs.py
Use --verify-only to check all runs or --export to save execution transcripts.
The viewer uses only the Python standard library.
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

try:
    from .teacher_cases import (comparable_teacher_output, comparison_description,
                                expectation, teacher_cases)
except ImportError:  # Support python3 -B tests/record_runs.py.
    from teacher_cases import (comparable_teacher_output, comparison_description,
                               expectation, teacher_cases)


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
            expected_path=None, expected_bytes=None, expected_source=None,
            teacher_output=False, description=None):
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
        expected_bytes = expected_path.read_bytes()
        expected_source = "Existing regression fixture: " + expected_path.relative_to(ROOT).as_posix()
    if expected_bytes is not None:
        if result.stderr:
            raise RuntimeError(f"{run_id} produced unexpected standard error")
        compare = comparable_teacher_output if teacher_output else normalized
        if compare(result.stdout) != compare(expected_bytes):
            raise RuntimeError(f"{run_id} does not match {expected_source}")
    command = "python3 -B " + " ".join(arguments)
    if input_path is not None:
        command += " < " + input_path.relative_to(ROOT).as_posix()
    if description is None:
        description = ("PASS — expected output verified" if expected_bytes is not None
                       else "PASS — command completed successfully")
    return {
        "id": run_id, "filename": run_id + ".jpg", "title": title,
        "path": "/run/" + run_id, "command": command,
        "input": None if input_bytes is None else normalized(input_bytes).decode("utf-8"),
        "stdout": normalized(result.stdout).decode("utf-8"),
        "stderr": normalized(result.stderr).decode("utf-8"),
        "status": result.returncode, "verified": expected_bytes is not None,
        "expected": None if expected_bytes is None else normalized(expected_bytes).decode("utf-8"),
        "expected_source": expected_source, "comparison": description,
        "teacher": teacher_output,
    }


def collect_runs(teacher_only=False):
    records = []
    if not teacher_only:
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
    for case in teacher_cases(ROOT):
        expected, provenance = expectation(case)
        source = ("Teacher answer: " + case.expected_path.relative_to(ROOT).as_posix()
                  if provenance == "teacher" else
                  "Independent mirrored-character reference; teacher answer "
                  + case.expected_path.name + " was not supplied")
        records.append(capture(
            case.run_id, f"Problem {case.problem} — {case.input_path.name}",
            [case.program], case.input_path.read_bytes(), case.input_path,
            expected_bytes=expected, expected_source=source, teacher_output=True,
            description=comparison_description(case, provenance),
        ))
    records.sort(key=lambda record: record["id"])
    if not teacher_only:
        records.append(capture(
            "tests_unittest", "Automated tests",
            ["-m", "unittest", "discover", "-s", "tests", "-v"],
            description="PASS — all automated tests completed successfully",
        ))
    return records


def export_runs(records):
    """Save actual teacher runs, the stack demonstration, and test results."""
    destination = ROOT / "example_executions"
    destination.mkdir(parents=True, exist_ok=True)
    selected = [record for record in records
                if record["teacher"] or record["id"] in ("p3_stacks", "tests_unittest")]
    for record in selected:
        sections = [record["title"],
                    "Actual subprocess execution · Python " + platform.python_version(),
                    "\nCommand:\n" + record["command"],
                    "\nVerification:\n" + record["comparison"],
                    "Exit status: " + str(record["status"])]
        if record["expected_source"] is not None:
            sections.append("Expected output origin: " + record["expected_source"])
        if record["input"] is not None:
            sections.append("\nInput:\n" + record["input"])
        sections.append("\nActual stdout:\n" + record["stdout"])
        if record["stderr"]:
            sections.append("\nActual stderr:\n" + record["stderr"])
        if record["expected"] is not None:
            sections.append("\nExpected output:\n" + record["expected"])
        with (destination / (record["id"] + ".txt")).open(
                "w", encoding="utf-8", newline="\n") as output:
            output.write("\n".join(sections) + "\n")
    return selected


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
@media (max-width: 600px) {
  body { padding: 18px 14px; } h1 { font-size: 22px; }
  pre { padding: 12px 10px; font-size: 13px; }
}
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
    if record["expected"] is not None:
        body += "<h2>Expected output</h2><pre>" + html.escape(record["expected"]) + "</pre>"
        body += "<div class='meta'>" + html.escape(record["expected_source"]) + "</div>"
    body += "<div class='status'>Exit status: " + str(record["status"])
    body += "<br>" + html.escape(record["comparison"])
    body += "</div>"
    return document(record["title"], body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--teacher-only", action="store_true",
                        help="Capture only the 29 teacher inputs")
    parser.add_argument("--export", action="store_true",
                        help="Write actual run transcripts to example_executions/ and exit")
    arguments = parser.parse_args()
    records = collect_runs(teacher_only=arguments.teacher_only)
    if arguments.export:
        exported = export_runs(records)
        print(f"Exported {len(exported)} actual execution transcripts to example_executions/.")
    if arguments.verify_only or arguments.export:
        print(f"Verified {len(records)} actual executions.")
        return
    lookup = {record["path"]: record for record in records}
    manifest = [{key: record[key] for key in ("id", "filename", "title", "path", "comparison", "teacher")}
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
