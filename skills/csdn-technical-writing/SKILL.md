---
name: csdn-technical-writing
description: "Draft, rewrite, or audit Chinese CSDN-style technical articles using a specific long-form teaching structure: a plain-text overall title, Markdown headings for section levels, dense natural paragraphs, beginner-first progression, commented code examples, and splitting when an article becomes too long. Use for technical tutorials, AI and backend articles, engineering practice notes, and beginner-friendly series."
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - technical-writing
    - chinese
    - csdn
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
7. Default to approximately **1,500–2,000 Chinese characters per article**, with a **3,000-character maximum** unless the user explicitly requests a longer article. Split broader topics into independently useful articles.
8. Preserve enough details, working mechanisms, and short commands for a reader to reproduce the core technique. Cut repetition and generic transitions before cutting actionable substance.

Run `scripts/lint_csdn_article.py` when the draft is available as Markdown.

## Private-project anonymization (default, before drafting)

Assume projects, client engagements, school/lab systems, deployments, and source material are **private or publication-restricted unless the user explicitly authorizes identifiable publication**. A publicly accessible repository, screenshot, or URL does not by itself authorize exposing additional project details in a blog.

Before writing public-facing CSDN text, replace or omit identifying details including:
- Real project/system names and unique aliases, organizations, schools, clients, team members, people, and internal project context.
- Public/private IP addresses, domains, host aliases, SSH usernames, ports used uniquely by the real deployment, instance IDs, and real environment paths, directory names, database/schema/table names.
- Credentials, tokens, passwords, private keys, private API endpoints, internal URLs, unpublished release versions, exact incidents/timestamps, data volumes, performance figures, unpublished architecture specifics, and proprietary model/dataset assets.
- Screenshots, code excerpts, log messages, and comments containing identifying details, including indirect combinations of details that make a project recognizable.

Use **generic runnable examples** instead: `example-app`, `app_db`, `app_user`, `<ECS_HOST>`, `/opt/example-app/`, illustrative ports, fictional filenames, sanitized code comments, and realistic placeholder values. State when a command or configuration is illustrative. Preserve generally reusable technology names and correct mechanisms (Spring Boot, Vue, Flask, Java, MySQL, Nginx, etc.). Never print real secret values even when a project is explicitly public.

For a private project, write a reusable engineering tutorial with anonymized scenarios and no traceable case identifiers. Mention a real project name, exact results, public URLs, or uniquely identifying repository links **only with explicit user authorization for those details**. If in doubt, generalize without asking the user for private information. Verify titles, prose, tables, code blocks, file paths, captions, and link destinations before publication.

Do not change the actual user's code, server configuration, or repository merely to anonymize a blog; anonymization applies to the published text and examples.

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
