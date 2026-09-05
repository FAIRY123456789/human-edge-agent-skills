---
name: csdn-technical-writing
description: "Draft, rewrite, or audit Chinese CSDN-style technical articles using a specific long-form teaching structure: plain-text overall title, Markdown H1/H2 only for section levels, dense natural paragraphs instead of many micro-paragraphs, beginner-first concept progression, commented code examples, and automatic splitting when a single article becomes too long. Use for technical tutorials, AI/backend articles, engineering practice notes, and beginner-friendly series."
---

# CSDN Technical Writing

Write for a motivated beginner who wants to understand the mechanism, not just copy the code.

## Formatting contract

1. The article's **overall title is plain text**, not a Markdown heading.
2. First-level sections use `#`.
3. Second-level sections use `##`.
4. Prefer roughly **4–7 first-level sections** for a normal article.
5. Use full natural paragraphs. Do not split every sentence into a separate paragraph.
6. Code goes in fenced code blocks.
7. When total content would exceed roughly **5,000 Chinese characters**, split it into a series rather than compressing explanation.
8. Code-heavy subarticles should generally stay within about **5,000 Chinese characters**. A deliberately concise version can target about **2,000 characters**.

Run `scripts/lint_csdn_article.py` when the draft is available as Markdown.

## Teaching sequence

For each important concept:

1. Give a formal, accurate definition.
2. Explain it again in natural language.
3. Explain how it works step by step.
4. Explain when it is useful.
5. Explain one or two common mistakes or misunderstandings.
6. Give a minimal but meaningful code example.
7. Comment key lines or explain them immediately after the code.
8. Connect the concept to the next concept before introducing new terminology.

Do not stack several unexplained terms in one paragraph.

## Paragraph style

- Prefer medium-to-long natural paragraphs when a concept needs continuous explanation.
- Short paragraphs are allowed when they improve code reading or mark a genuine transition.
- Avoid list-heavy article bodies when prose can explain the logic more naturally.
- Avoid repetitive heading formulas such as “为什么……是什么……应该怎样……”. Headings should name the actual technical issue.
- Keep language professional, clear, and approachable. Avoid empty motivational sentences and generic AI conclusions.

## Article series

If one topic needs several articles, preserve a clear learning path. Each subarticle should solve one coherent stage and state what prerequisite it assumes.
