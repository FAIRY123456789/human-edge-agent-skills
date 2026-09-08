#!/usr/bin/env python3
"""Check a Markdown draft against the CSDN article structure used by this Skill."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MIN_H1 = 4
MAX_H1 = 7
MIN_PARAGRAPH_CHARS = 45
MAX_SHORT_PARAGRAPH_RATIO = 0.45
MAX_CJK_CHARS = 5000


def inspect_article(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"article not found: {path}")
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues: list[str] = []

    nonempty = [line for line in lines if line.strip()]
    if nonempty and nonempty[0].lstrip().startswith("#"):
        issues.append("Overall article title should be plain text, not a Markdown heading.")

    h1 = [line for line in lines if re.match(r"^# ", line)]
    h3 = [line for line in lines if re.match(r"^#{3,} ", line)]
    if not (MIN_H1 <= len(h1) <= MAX_H1):
        issues.append(f"H1 count is {len(h1)}; normal target is roughly {MIN_H1}-{MAX_H1}.")
    if h3:
        issues.append("Found H3+ headings. This house style normally uses an overall title, H1, and H2.")

    clean: list[str] = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            clean.append(line)
    plain = "\n".join(clean)
    paragraphs = [
        re.sub(r"\s+", "", paragraph)
        for paragraph in re.split(r"\n\s*\n", plain)
        if paragraph.strip() and not paragraph.lstrip().startswith("#")
    ]
    short_count = sum(1 for paragraph in paragraphs if len(paragraph) < MIN_PARAGRAPH_CHARS)
    if paragraphs and short_count / len(paragraphs) > MAX_SHORT_PARAGRAPH_RATIO:
        issues.append(
            f"{short_count}/{len(paragraphs)} prose paragraphs are under "
            f"{MIN_PARAGRAPH_CHARS} characters; check for excessive micro-paragraphs."
        )

    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    if cjk_count > MAX_CJK_CHARS:
        issues.append(f"Article contains about {cjk_count} CJK characters; consider splitting into a series.")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    args = parser.parse_args()
    issues = inspect_article(args.article)
    if issues:
        print("Style review:")
        for issue in issues:
            print("-", issue)
        return 1
    print("No obvious CSDN house-style issues found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
