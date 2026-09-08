# ASR Context Resolution

Speech recognition often corrupts proper nouns, company/project names, acronyms, model names, and technical terms. Correct them only when several signals converge.

## Candidate sources, strongest first

1. Exact named entity already established in the active conversation or project.
2. User-supplied glossary or repository terminology.
3. A term repeated several times in the same transcript.
4. Phonetic/homophone similarity.
5. Semantic role consistency: does the candidate make sense as a company, model, file, person, product, API, etc.?
6. Sentence and paragraph coherence after substitution.

## Confidence rule

### High confidence — normalize
Use when the candidate is already established and the phonetic/semantic fit is strong.

Example pattern:
`成舟台` → `澄舟台` when the fictional term `澄舟台` is already established in active context and the corrected sentence becomes semantically coherent.

### Medium confidence — expose assumption
Write:
`Assumption: “X” is likely “Y” because ...`

### Low confidence — preserve and flag
Do not guess.

## Frequency is evidence, not proof

A term appearing often in memory/context gets more weight, especially if it is a high-status named entity in the current project. Still require phonetic and semantic consistency.

## Privacy rule

Do not pull unrelated names from private memory merely to make a public or shared transcript look cleaner. Use memory only when the host exposes it appropriately and the current task context makes the reference relevant.
