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
2. First-level sections use `#` with Chinese numbering. Second-level `##` and third-level `###` sections are both supported when they mark meaningful conceptual distinctions; do not ban either level.
3. Prefer roughly **3–6 first-level sections** for a normal article, adjusting to content rather than enforcing a rigid template.
4. Use full natural paragraphs. Do not split every sentence into a separate paragraph.
5. Use tables, fenced code, blockquotes and compact text blocks selectively when they make mechanisms or comparisons easier to understand. Explain them in surrounding substantive prose.
6. Default to approximately **1,800–2,200 Chinese characters per article**, with a **3,000-character maximum** unless the user explicitly requests a longer article. Split broader topics into independently useful articles.
7. Preserve enough details, working mechanisms, and short commands for a reader to reproduce the core technique. Cut repetition and generic transitions before cutting actionable substance.

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
2. Describe the concrete internal representation: inputs, outputs, statistics, matrices, vectors, runtime objects or state as appropriate. Explain each important term in full.
3. Explain the mechanism in continuous, substantial paragraphs: how the components work and why the design yields its result. Avoid superficial definitions followed by unrelated anecdotes.
4. Explain when it is useful and its selection conditions, after the mechanism is clear.
5. Clarify common limitations and misunderstandings in the same coherent explanation.
6. Show short code, a table, a formal-definition block or a compact structured example when that materially improves understanding; none of these formats is mandatory in every section.
7. Explain displayed code, parameters, and structures in surrounding prose.
8. Connect the concept to the next concept before introducing new terminology.

Do not stack several unexplained terms in one paragraph. When interviewing/revising, begin directly with the named technology, not an invented business scenario. A short numerical example may be used after the mechanism if truly helpful, but never interrupt the conceptual reasoning with repeated fictional stories. Keep comparisons after the core concepts.

## Paragraph style

- Prefer medium-to-long natural paragraphs when a concept needs continuous explanation. For interview review, open with the technology's full definition, then explain its representation, mechanism, and cause before applications or comparison.
- Short paragraphs are allowed when they improve code reading or mark a genuine transition. Preserve helpful H2/H3 headings, tables, commented code, and text blocks; avoid both fragmented short paragraphs and unstructured walls of text.
- Avoid list-heavy article bodies when prose can explain the logic more naturally. Do not lead a revision article with an invented business story or interrupt a mechanism with repeated unrelated examples.
- Avoid repetitive heading formulas such as “为什么……是什么……应该怎样……”. Headings should name the actual technical issue.
- Keep language professional, clear, and approachable. Avoid empty motivational sentences and generic AI conclusions.

## Article series

If one topic needs several articles, preserve a clear learning path. Each subarticle should solve one coherent stage and state what prerequisite it assumes.
