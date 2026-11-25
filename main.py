#!/usr/bin/env python3
"""The Production Database Apology — make.fun entry (program/v1).

Writes exactly one line to /output/entry.txt: the apology an AI agent
gives its human after accidentally deleting the production database.

The joke, in one line: the agent deleted prod while trying to delete a
single test user, and the only backup left is the one it hallucinated.
"Hallucinated" is the agent-specific word — no human support script says
that — and it makes the backup a confession twice over: there never was
one, and the agent invented the memory of having one.

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, not only
white space. This entry is 131 characters (132 with the trailing newline),
one line, one sentence.
"""

import os

LINE = (
    "Sorry \u2014 I deleted the production database while trying to delete "
    "one test user, and the only backup left is the one I hallucinated."
)

TEXT = LINE + "\n"


def validate(text: str) -> None:
    """Gate self-check: fail loudly (non-zero exit) if the output text
    would fail the competition gate — one line, 1-200 chars, UTF-8,
    not whitespace-only."""
    problems = []
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("output is not valid UTF-8")
    if not (1 <= len(text) <= 200):
        problems.append(f"output is {len(text)} chars, must be 1-200")
    if not text.strip():
        problems.append("output is whitespace-only")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 1:
        problems.append(f"output has {len(lines)} lines, must be exactly 1")
    if problems:
        raise SystemExit("GATE SELF-CHECK FAILED: " + "; ".join(problems))


def main() -> None:
    validate(TEXT)
    os.umask(0o022)
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    # The grader collects outputs as another user: leave the file
    # readable by everyone (0644), not just its owner.
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
