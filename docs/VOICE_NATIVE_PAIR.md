# Voice Native Pair

## Shared problem

Modern voice input is fast but noisy. The user may speak project names, model names, acronyms, people, dates, and corrections faster than ASR can reliably transcribe them.

Both `voice-dump-to-todo` and `vibe-to-spec` use context-aware repair:

`raw ASR → active glossary → candidate correction → semantic self-check → confidence → normalized output`

## Different destination

### voice-dump-to-todo
Question: **What needs to happen?**

Output: Action / Decision / Waiting / Later, priority, dependency, due date, definition of done, standalone HTML.

### vibe-to-spec
Question: **What should the software do?**

Output: product goal, scope, user flow, data/state, interfaces, constraints, acceptance criteria, implementation order.

## Example

Raw transcript contains a recurring company/project term as a homophone. If the canonical name already appears repeatedly in the active project context, the phonetics fit, and the corrected sentence becomes meaningfully more coherent, the agent can normalize it with high confidence.

The system must still preserve ambiguity when the candidate could refer to two different entities.
