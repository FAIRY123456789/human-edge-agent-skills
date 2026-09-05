---
name: voice-dump-to-todo
description: "Convert a long, messy, repetitive, speech-recognition-heavy task dump into a precise executable to-do list. Use when the user speaks tasks in inaccurate ASR language, changes priorities mid-sentence, mixes ideas with actions, or wants a downloadable standalone interactive HTML to-do that can be saved or dragged to the desktop. Use context-aware named-entity repair when a recurring term is clearly misrecognized, preserve uncertain corrections, and produce concrete definitions of done."
---

# Voice Dump to Todo

The input can be chaotic. The output must be executable.

## This skill is not `vibe-to-spec`

Use **voice-dump-to-todo** when the destination is a personal or team action list: what to do, decide, wait for, schedule, or park.

Use **vibe-to-spec** when the voice dump describes a product, system, feature, code change, webpage, API, or technical build and the destination is an implementation specification.

## Workflow

1. Read the whole dump before extracting tasks. Later sentences may correct earlier ASR errors, dates, priorities, or scope.
2. Build a small active glossary from terms already established in the current conversation/project, explicit user glossaries, repeated names in the transcript, and host-provided memory only when it is legitimately available and relevant.
3. Resolve suspicious ASR terms using `references/asr-context-resolution.md`. Do not “correct” a rare unknown name just because a familiar name exists in memory.
4. Split content into:
   - **Action** — something someone should do;
   - **Decision** — a choice that must be made;
   - **Waiting** — blocked by another person/event;
   - **Later** — useful idea with no current commitment;
   - **Background** — context that should not become a task.
5. For every Action, produce:
   - concise verb-first title;
   - concrete definition of done;
   - owner when known;
   - priority;
   - due date or time window only if actually stated or safely derived from an explicit relative date;
   - dependency;
   - uncertainty note when needed.
6. Merge duplicates and use later explicit corrections to override earlier versions.
7. Preserve task order when it encodes dependency. Otherwise rank by consequence and timing.
8. Keep the active list small. Do not convert every reflection into a P0 task.
9. When file output is requested, write a JSON task file and run `scripts/render_todo.py` to create a standalone interactive HTML file using localStorage.
10. End with a short `Needs confirmation` section only when unresolved details materially affect execution.

## Default task schema

```json
{
  "title": "Verb-first task",
  "details": "Definition of done",
  "owner": "",
  "priority": "P1",
  "due": "",
  "status": "todo",
  "depends_on": [],
  "uncertainty": ""
}
```

## Output modes

- Compact Markdown checklist
- Structured JSON
- Standalone interactive HTML using localStorage

Do not turn reflective thoughts into tasks unless an action is explicitly implied.
