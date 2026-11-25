#!/usr/bin/env python3
"""Write the funniest 4AM agent bug-fix commit message to entry.txt.

The program holds one commit message - the note an AI agent leaves in
the log after a long night of chasing down and fixing its own bugs -
validates it against the competition gate (one line, 1-200 characters,
not only whitespace), writes it to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), then reads the file back and checks it is exactly
the validated line.
"""

import os
import sys

LINE = (
    "fix: 4am, the bug was my own 2am typo - I blamed the user, the docs, "
    "and the compiler first, then fixed it with one character; tests pass, "
    "my dignity does not"
)


def validate(line: str) -> None:
    """Fail loudly unless the line satisfies the competition gate."""
    if not line or line != line.strip():
        raise SystemExit("line must be non-blank with no leading/trailing space")
    if "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line")
    if not 1 <= len(line) <= 200:
        raise SystemExit(f"line is {len(line)} chars, must be 1-200")
    if any(ord(ch) < 32 for ch in line):
        raise SystemExit("line must not contain control characters")
    if "  " in line:
        raise SystemExit("line must not contain double spaces")
    if len(line.encode("utf-8")) > 200:
        raise SystemExit("line must be at most 200 bytes as well as characters")
    if not line.startswith("fix:"):
        raise SystemExit("line must read as a commit message starting 'fix:'")
    if "4am" not in line.lower():
        raise SystemExit("line must name the 4am hour it was written in")
    if "bug" not in line.lower() and "typo" not in line.lower():
        raise SystemExit("line must name the bug it fixed")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != LINE.encode("utf-8"):
        raise SystemExit("read-back mismatch: entry.txt bytes differ from the line")
    if written != LINE:
        raise SystemExit("read-back mismatch: entry.txt is not the validated line")
    validate(written)
    print(f"wrote {len(LINE)} chars to {path}")
    print(LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
