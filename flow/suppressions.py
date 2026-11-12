#!/usr/bin/env python3
"""Blocks new suppression comments: `# noqa`, `@ts-ignore`, `eslint-disable` and friends.

Only lines the pull request *adds* are counted, so existing suppressions in a
repository do not fail every later pull request. Runs in GitHub Actions.

Usage:
    python flow/suppressions.py --base SHA --head SHA [--repo-root DIR]
    python flow/suppressions.py --diff-file FILE    # a unified diff on stdin or in a file
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = (
    ("# noqa", re.compile(r"#\s*noqa", re.I)),
    ("# type: ignore", re.compile(r"#\s*type:\s*ignore", re.I)),
    ("# pylint: disable", re.compile(r"#\s*pylint:\s*disable", re.I)),
    ("@ts-ignore", re.compile(r"@ts-ignore")),
    ("@ts-expect-error", re.compile(r"@ts-expect-error")),
    ("eslint-disable", re.compile(r"eslint-disable")),
    ("prettier-ignore", re.compile(r"prettier-ignore")),
)
FILE_HEADER = re.compile(r"^\+\+\+ b/(.*)$")
HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
# The suppressions file itself names every pattern; so does its test.
EXEMPT = ("flow/suppressions.py", "flow/test_suppressions.py", "flow/FLOW.md", "flow/ci/")


def exempt(path: str) -> bool:
    return any(path == item or path.startswith(item) for item in EXEMPT)


def find_added(diff: str) -> list[tuple[str, int, str, str]]:
    """(path, line number in the new file, pattern name, the added line) for each hit."""
    hits: list[tuple[str, int, str, str]] = []
    path, line_number = "", 0
    for raw in diff.splitlines():
        header = FILE_HEADER.match(raw)
        if header:
            path, line_number = header.group(1), 0
            continue
        hunk = HUNK_HEADER.match(raw)
        if hunk:
            line_number = int(hunk.group(1))
            continue
        if raw.startswith("+++") or raw.startswith("---") or not path:
            continue
        if raw.startswith("+"):
            content = raw[1:]
            if not exempt(path):
                for name, pattern in PATTERNS:
                    if pattern.search(content):
                        hits.append((path, line_number, name, content.strip()))
                        break
            line_number += 1
        elif not raw.startswith("-"):
            line_number += 1
    return hits


def git_diff(base: str, head: str, root: Path) -> str:
    result = subprocess.run(
        ["git", "diff", "-U0", "--no-color", "--no-renames", base, head, "--"],
        cwd=root, capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode:
        raise SystemExit(f"FAIL: git diff {base}..{head}: {result.stderr.strip()}")
    return result.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--diff-file", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    if args.diff_file:
        diff = args.diff_file.read_text(encoding="utf-8")
    elif args.base and args.head:
        diff = git_diff(args.base, args.head, args.repo_root)
    else:
        parser.error("give --base and --head, or --diff-file")

    hits = find_added(diff)
    if not hits:
        print("PASS: the diff adds no suppression comment")
        return 0
    print(f"FAIL: the diff adds {len(hits)} suppression comment(s). Fix the code instead.")
    for path, line, name, content in hits:
        print(f"  {path}:{line}: {name} — {content}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
