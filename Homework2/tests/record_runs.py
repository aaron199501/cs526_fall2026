"""Verify instructor examples and save actual execution transcripts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

from teacher_cases import load_teacher_cases


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Execution:
    id: str
    title: str
    args: list[str]
    input_path: str | None
    expected: str | None
    comparison: str
    teacher: bool
    screenshot: str | None
    stdout: str = ''
    stderr: str = ''
    exit_code: int = -1
    verified: bool = False


def normalized(text):
    return text.replace('\r\n', '\n').removesuffix('\n')


def collect_runs(root=ROOT):
    root = Path(root)
    cases = []
    for case in load_teacher_cases(root):
        reference = case['reference']
        source = reference.get('path', reference.get('filename', 'instructor transcript'))
        cases.append(Execution(
            'teacher_' + case['id'], case['title'], case['args'],
            case['input_path'], case['expected_stdout'],
            'matches instructor output in ' + source, True,
            'teacher_' + case['id'] + '.jpg'))
    cases.extend([
        Execution('problem2_all_operations', 'Problem 2 — original all-directive fixture',
                  ['problem2_driver.py'], 'problem2Resources/problem2_all_operations.txt',
                  None, 'additional saved input completed successfully', False,
                  'problem2_all_operations.png'),
        Execution('problem3', 'Problem 3 — required 3, 5, and 10 step counts',
                  ['problem3.py'], None,
                  'ways(3) = 4\nways(5) = 13\nways(10) = 274\n',
                  'matches the required staircase counts', False, 'problem3.png'),
        Execution('problem4', 'Problem 4 — original sorted-list demonstration',
                  ['problem4.py'], None, None,
                  'original demonstration completed successfully; list methods checked by unittest',
                  False, 'problem4.png'),
        Execution('tests_unittest', 'Automated tests',
                  ['-m', 'unittest', 'discover', '-s', 'tests', '-v'], None, None,
                  'all automated tests completed successfully', False, 'tests_unittest.png'),
    ])
    for filename in ('tests/original_resources/problem2_basic.txt',
                     'tests/original_resources/problem2_errors.txt',
                     'problem2Resources/problem2_empty_single.txt'):
        cases.append(Execution('supplemental_' + Path(filename).stem,
                               'Problem 2 — retained original fixture: ' + Path(filename).name,
                               ['problem2_driver.py'], filename, None,
                               'retained original input completed successfully', False, None))
    for case in cases:
        input_bytes = (root / case.input_path).read_bytes() if case.input_path else None
        process = subprocess.run([sys.executable, '-B', *case.args], cwd=root,
                                 input=input_bytes, capture_output=True, timeout=60)
        case.stdout = process.stdout.decode('utf-8')
        case.stderr = process.stderr.decode('utf-8')
        case.exit_code = process.returncode
        is_test = case.id == 'tests_unittest'
        case.verified = process.returncode == 0 and (is_test or not case.stderr)
        if case.expected is not None:
            case.verified = case.verified and normalized(case.stdout) == normalized(case.expected)
        if is_test:
            case.verified = case.verified and bool(re.search(r'Ran \d+ tests[\s\S]*\nOK\r?\n', case.stderr))
    return cases


def transcript(case):
    command = 'python3 -B ' + ' '.join(case.args)
    if case.input_path:
        command += ' < ' + case.input_path
    lines = [case.title, 'Command: ' + command]
    if case.input_path:
        lines.append('Standard input: ' + case.input_path)
    lines.extend(['', 'Actual output:', case.stdout.replace('\r\n', '\n').rstrip('\n')])
    if case.stderr:
        lines.extend(['', 'Standard error:', case.stderr.replace('\r\n', '\n').rstrip('\n')])
    lines.extend(['', 'Exit code: ' + str(case.exit_code),
                  ('PASS: ' if case.verified else 'FAIL: ') + case.comparison, ''])
    return '\n'.join(lines)


def export_runs(cases, root=ROOT):
    folder = Path(root) / 'example_executions'
    folder.mkdir(exist_ok=True)
    count = 0
    for case in cases:
        if case.screenshot:
            (folder / (case.id + '.txt')).write_text(transcript(case), encoding='utf-8')
            count += 1
    process = subprocess.run([sys.executable, '-B', 'problem3.py', '--teacher-examples'],
                             cwd=root, capture_output=True, timeout=60)
    expected = (Path(root) / 'tests/teacher_resources/problem3Excutions.txt').read_text(encoding='utf-8')
    actual = process.stdout.decode('utf-8')
    if process.returncode or process.stderr or normalized(actual) != normalized(expected):
        raise RuntimeError('Combined staircase examples did not match the instructor transcript.')
    combined = Execution('problem3_teacher_examples', 'Problem 3 — complete instructor examples',
                         ['problem3.py', '--teacher-examples'], None, expected,
                         'matches instructor problem3Excutions.txt', True, None,
                         actual, '', 0, True)
    (folder / 'problem3_teacher_examples.txt').write_text(transcript(combined), encoding='utf-8')
    return count + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='run and verify without exporting files')
    parser.add_argument('--export', action='store_true', help='also save actual execution transcripts')
    options = parser.parse_args()
    cases = collect_runs()
    for case in cases:
        print(('PASS' if case.verified else 'FAIL') + ': ' + case.id)
    failed = [case for case in cases if not case.verified]
    if failed:
        for case in failed:
            print(transcript(case), file=sys.stderr)
        return 1
    print(f'All {len(cases)} executions verified; {sum(case.teacher for case in cases)} instructor examples.')
    if options.export:
        print(f'Exported {export_runs(cases)} actual execution transcripts.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
