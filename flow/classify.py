#!/usr/bin/env python3
"""Flow level: `standard` or `elevated`, decided from the changed paths alone.

The script decides, not the agent and not a hand-typed label. The `flow-classify` job
in `flow/ci/flow-checks.yml` re-runs it on every push, so an agent cannot lower the
level of its own pull request: the label is overwritten with what this file says.

Rule: one elevated path makes the whole pull request elevated. A *new* test is
standard; changing or deleting an existing test is elevated.

Usage:
    python flow/classify.py --base SHA --head SHA [--repo-root DIR] [--github-output FILE]
    python flow/classify.py --changes-file FILE   # `git diff --name-status` output
    python flow/classify.py --budget              # process-code line count for flow/
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

STANDARD = "standard"
ELEVATED = "elevated"
LINE_BUDGET = 2500

# Whole trees that govern how the studio works.
ELEVATED_PREFIXES = (".github/", ".codex/", ".claude/", ".circleci/", "flow/", "orchestrator/")
# Exact file names, matched on the basename, lowercased.
ELEVATED_NAMES = {
    "repos.json", "codeowners", "dockerfile", "vercel.json", "netlify.toml",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "requirements.txt", "requirements-dev.txt", "pyproject.toml", "poetry.lock",
    "pipfile", "pipfile.lock", "go.mod", "go.sum", "cargo.toml", "cargo.lock",
    "gemfile", "gemfile.lock", "schema.prisma",
}
# Directory names anywhere in the path.
ELEVATED_SEGMENTS = {"migrations", "migration", "auth"}
# Secrets and credentials, matched on the basename.
SECRET_RE = re.compile(r"(^|[._-])(env|secret|secrets|credential|credentials|keystore)([._-]|$)", re.I)
# Data schema files.
SCHEMA_SUFFIXES = (".sql", ".prisma")
SCHEMA_RE = re.compile(r"(^|[._-])schema([._-]|$)", re.I)
# Tests. A new one is standard; touching an existing one is not.
TEST_SEGMENTS = {"tests", "test", "__tests__", "spec"}
TEST_NAME_RE = re.compile(r"(^test_.*\.py$|_test\.py$|\.(test|spec)\.[jt]sx?$|^test_.*\.[jt]sx?$)", re.I)
ADDED = "A"


def is_test(path: str) -> bool:
    pure = PurePosixPath(path)
    return bool(TEST_SEGMENTS & set(pure.parts[:-1])) or TEST_NAME_RE.search(pure.name) is not None


def reasons_for(status: str, path: str) -> list[str]:
    """Why this one change is elevated. Empty list means the change is standard."""
    pure = PurePosixPath(path)
    name = pure.name.lower()
    found = []
    for prefix in ELEVATED_PREFIXES:
        if path.startswith(prefix):
            found.append(f"{path}: governance tree {prefix}")
    if name in ELEVATED_NAMES:
        found.append(f"{path}: configuration or dependency manifest")
    segments = {part.lower() for part in pure.parts[:-1]}
    for segment in sorted(ELEVATED_SEGMENTS & segments):
        found.append(f"{path}: {segment}/ directory")
    if SECRET_RE.search(name):
        found.append(f"{path}: secrets or credentials")
    if pure.suffix.lower() in SCHEMA_SUFFIXES or SCHEMA_RE.search(name):
        found.append(f"{path}: data schema")
    if is_test(path) and status != ADDED:
        found.append(f"{path}: existing test changed or deleted ({status})")
    return found


def classify(changes: list[tuple[str, str]]) -> tuple[str, list[str]]:
    """changes: (status, path) pairs, status as `git diff --name-status` reports it."""
    reasons = [reason for status, path in changes for reason in reasons_for(status, path)]
    return (ELEVATED if reasons else STANDARD), reasons


def parse_name_status(text: str) -> list[tuple[str, str]]:
    """Parses `git diff --name-status -z`. A rename reports both of its paths."""
    fields = [field for field in text.split("\0")]
    changes: list[tuple[str, str]] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index].strip()
        if not status:
            break
        count = 2 if status[0] in "RC" else 1
        for path in fields[index + 1:index + 1 + count]:
            if path:
                changes.append((status[0], path))
        index += 1 + count
    return changes


def git_changes(base: str, head: str, root: Path) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "diff", "--name-status", "-z", "--find-renames", base, head, "--"],
        cwd=root, capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode:
        raise SystemExit(f"FAIL: git diff {base}..{head}: {result.stderr.strip()}")
    return parse_name_status(result.stdout)


def process_lines(root: Path) -> list[tuple[Path, int]]:
    """Process code under flow/: Python without tests. Documents and CI yaml are not code."""
    counted = []
    for path in sorted((root / "flow").rglob("*.py")):
        if path.name.startswith("test_"):
            continue
        counted.append((path, len(path.read_text(encoding="utf-8").splitlines())))
    return counted


def budget_report(root: Path) -> tuple[int, str]:
    counted = process_lines(root)
    total = sum(lines for _, lines in counted)
    body = "\n".join(f"  {path.relative_to(root).as_posix()}: {lines}" for path, lines in counted)
    verdict = "OK" if total <= LINE_BUDGET else "OVER BUDGET"
    return total, f"flow/ process code: {total}/{LINE_BUDGET} lines — {verdict}\n{body}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--changes-file", type=Path, help="git diff --name-status output, NUL or newline separated")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--github-output", type=Path, help="append level=... and reason=... for Actions")
    parser.add_argument("--budget", action="store_true", help="print the flow/ process-code line count")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    if args.budget:
        total, text = budget_report(args.repo_root)
        print(text)
        return 0 if total <= LINE_BUDGET else 1

    if args.changes_file:
        raw = args.changes_file.read_text(encoding="utf-8")
        changes = parse_name_status(raw if "\0" in raw else raw.replace("\t", "\0").replace("\n", "\0"))
    elif args.base and args.head:
        changes = git_changes(args.base, args.head, args.repo_root)
    else:
        parser.error("give --base and --head, or --changes-file, or --budget")

    level, reasons = classify(changes)
    summary = reasons[0] if reasons else f"{len(changes)} changed path(s), none elevated"
    print(f"level={level}")
    print(f"reason={summary}")
    for reason in reasons:
        print(f"  {reason}")
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"level={level}\nreason={summary}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
