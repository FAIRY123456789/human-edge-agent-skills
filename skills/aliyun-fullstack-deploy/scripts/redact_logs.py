#!/usr/bin/env python3
"""Redact common credentials and authorization headers from logs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{12,}"), "[REDACTED_API_KEY]"),
    (re.compile(r"(?im)^(\s*[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|DATABASE_URL|PRIVATE_URL)\s*=).*$"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)[^\s]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(ssh://[^@\s]+@)[^/:\s]+"), r"\1[REDACTED_HOST]"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.S), "[REDACTED_PRIVATE_KEY]"),
]


def redact(text: str) -> str:
    """Return text with supported credential forms removed."""
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8", errors="replace") if args.input else sys.stdin.read()
    text = redact(text)
    if args.output:
        args.output.write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
