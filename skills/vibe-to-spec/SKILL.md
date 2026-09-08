---
name: vibe-to-spec
description: "Convert messy voice input, imperfect speech recognition, half-formed product ideas, and iterative corrections into an implementation-ready software specification for Codex, Claude Code, Copilot, Cursor, or another coding agent. Use when the user speaks faster than they structure requirements, named entities are misrecognized, context or memory can safely resolve recurring terms, and the final output needs scope, flows, data, constraints, acceptance tests, and explicit unknowns rather than a raw transcript."
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - specifications
    - voice-input
    - software-development
---

# Vibe to Spec

## Purpose

The user's speech can be fuzzy. The implementation contract cannot be. Recover intent without hiding consequential uncertainty or inventing remembered context.

## This skill is not `voice-dump-to-todo`

Use **vibe-to-spec** when the destination is a product, feature, code change, system, webpage, API, or technical build.

Use **voice-dump-to-todo** when the destination is the user's personal execution list: tasks, decisions, waiting items, deadlines, and an interactive to-do.

## Instructions

1. Read the entire voice dump before normalizing anything. Later sentences often correct earlier ASR errors or change scope.
2. Build an **active glossary** from:
   - exact terms repeated in the current input;
   - named entities in the active conversation or project context;
   - user-provided glossaries or files;
   - host-provided memory only when the product legitimately exposes it and the user would reasonably expect it to be used.
3. Resolve suspicious ASR terms with `references/asr-context-resolution.md`.
4. Maintain a correction ledger for meaningful corrections. High-confidence corrections can be normalized silently in the spec; medium-confidence corrections must remain visible as assumptions; low-confidence terms remain unresolved.
5. Recover intent in layers:
   - goal and target user;
   - current problem;
   - in-scope behaviors;
   - explicit out-of-scope items;
   - user flow;
   - screens and components;
   - data and entities;
   - integrations and APIs;
   - constraints and non-negotiables;
   - acceptance tests;
   - open questions that genuinely block implementation.
6. Convert subjective language into testable behavior. “更好看” needs design direction or reference; “更快” needs a measurable threshold or a marked unknown.
7. Preserve the user's corrections and vetoes. Later explicit corrections override earlier inferred intent.
8. Do not ask questions that the context can already answer. Ask only when ambiguity changes architecture, data loss risk, cost, security, or acceptance.
9. Produce the implementation pack using `assets/SPEC_TEMPLATE.md`.
10. End with a `Ready for coding agent` status: `YES`, `YES_WITH_ASSUMPTIONS`, or `NO_BLOCKED`.

## Output

Default deliverable:

- normalized brief;
- correction ledger for non-trivial ASR fixes;
- implementation specification content;
- acceptance criteria;
- assumptions and open blockers;
- suggested implementation order.

Never invent a remembered project name merely because it sounds plausible.

## Examples

- Input: a voice transcript that first says “mobile page,” later corrects it to a responsive web dashboard, and leaves the export format uncertain.
- Output: the corrected scope, a visible export-format assumption, user flows, data entities, acceptance tests, and `YES_WITH_ASSUMPTIONS` readiness.

## Limitations

Do not resolve names from memory when the host does not legitimately expose that context. Do not mark a specification ready when ambiguity changes architecture, cost, security, or data-loss risk.

## Troubleshooting

If corrections conflict, prefer the latest explicit correction and record the conflict. If the requested behavior cannot be tested, rewrite it as an observable outcome or leave it as an open blocker.
