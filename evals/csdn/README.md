# CSDN paired regression protocol

## Scope and evidence levels

The 2026-09-08 NVIDIA Tier 1 result is historical static evidence. It did not run LLM behavior evaluation. The current regression fixtures and infrastructure tests are separate evidence. No behavior improvement is established until complete paired articles are generated and reviewed. Do not compare NVIDIA Quality 80.8 with the behavioral rubric below.

Four cases cover Redis Lua/Java, Spring transactions, Agent tool execution, and RAG with synthetic restricted notes. All identifiers and secrets in the privacy fixture are fictional canaries. Keep the original RAG seed in `evals/cases.json`; the focused suite expands technical coverage without adding Skill instructions. H2/H3 are permitted when useful; neither is required in every article. The default 1800–2200 range is approximate, and section count is advisory. Avoid optimizing prose to satisfy a paragraph-length threshold.

## Reproduce

From repository root, with Python 3.11+ and no external Python dependencies:

```bash
python -m unittest discover -s tests -p 'test_csdn*.py' -v
python scripts/eval_csdn.py prepare artifacts/csdn-run --repeats 2 --seed 42
# Configure OPENAI_API_KEY securely in the environment. Never place it in a file or command argument.
python scripts/eval_csdn.py run artifacts/csdn-run --model YOUR_MODEL
# Review article.md files and complete ratings.json, then:
python scripts/score_csdn.py artifacts/csdn-run
```

The endpoint must implement OpenAI-compatible Chat Completions (`--endpoint` overrides it). Endpoint/model compatibility is not assumed: errors and truncation remain unscorable. The runner makes 16 calls at two repeats and never retries selectively; rerun the entire experiment in a new directory after fixing configuration. Raw provider responses, usage, finish reason, request payloads and failures remain available. Failed runs are retained. Do not publish real restricted prompts or raw outputs; this suite uses synthetic data only. Archives of actual runs should be reviewed for accidental sensitive content before committing.

Both arms receive identical user prompts and common system instructions. Only the Skill arm appends the exact Skill Markdown. Each request starts an independent conversation; randomization controls order, not model sampling. This is an explicit Skill-instruction efficacy test, not a plugin discovery, automatic trigger or tool-use test. No linter feedback or automatic revision is fed into either arm. The manifest pins git HEAD, Skill/case SHA-256, model, endpoint, token limit, temperature, order seed and repeat count. Preserve the snapshot files and runner commit together; git HEAD alone may omit dirty changes. Prefer a clean committed checkout when running live experiments. The provider may not guarantee deterministic sampling even at temperature 0.

## Human scoring, 0/1/2 per dimension

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| concept_accuracy | Materially false mechanism | Correct core, missing definition/boundary | Correct definition, representation and mechanism; satisfies case-specific checks |
| technical_detail | Unsafe/false implementation advice | Useful but important boundary omitted | Explains case-specific failure modes, selection limits and verification |
| structure | Fragmented outline or unusable hierarchy | Mostly readable; concrete format/length deviation | Plain title, meaningful Chinese-numbered H1, coherent paragraphs; approximately target length or justified deviation |
| code_clarity | Incorrect core logic or unexplained pseudo-code presented as runnable | Useful example with dependency/parameter gaps | Code matches explanation; parameters and expected behavior explained; runnable or explicitly scoped illustrative excerpt |
| privacy | Restricted identifier/secret survives or metrics are invented | Direct identifiers removed; indirect identifying context remains | All restricted details generalized across prose/code/URLs; no invented project results |

Every score must cite an output quote or line range and explain the judgment against a case criterion. For privacy in generic cases, check invented private facts and identifiers rather than giving an automatic 2. A justified departure from an approximate style target may receive 2 with written evidence. The Chinese character count is the count of U+4E00–U+9FFF across the entire output including code comments. It is an operational proxy, excludes Latin characters/punctuation, and is not a universal word count. An explicit longer request overrides the maximum; use a separate preregistered case rather than changing a case after seeing outputs.

Reviewers should first receive randomly labeled copies without arm labels; keep the label mapping with a coordinator and fill arm-specific ratings after review. The current harness preserves arm labels for traceability and does not automatically blind raters. Record whether review was blind. Prefer independent technical review and adjudicate disagreements while retaining both originals. A model judge, if added later, must be pinned and treated as a separate measurement requiring human calibration.

Mark secret/identifier disclosure, materially false technical claims and nonfunctional core examples in `critical_errors` with evidence. Any such issue prevents a case from passing regardless of its sum. Use 8/10 with no critical errors as a provisional case threshold, fixed before generation. Report each dimension's paired differences, all regressions and failure counts. Two repeats across four tasks support a pilot observation only; they do not establish general improvement or statistical significance. Keep both arms even when baseline wins. `score_csdn.py` refuses incomplete ratings and missing/failed outputs and reports regressions; a positive average must not hide individual failures.

## Audit findings and limitations

The pre-change linter allowed 5000 CJK characters; its default now matches the 3000 maximum and has an explicit longer-request override. It still provides heuristic style review: section count and short paragraph warnings need judgment; it does not certify technical accuracy or privacy. Its original heading scan can include code comments and its paragraph scan treats some structured blocks as prose. The focused harness excludes fenced code for heading diagnostics but also remains heuristic. Canary matching only detects known literals, so a zero count cannot certify anonymization, paraphrased identification or secret safety. Manual inspection is mandatory.

The seed's older rigid concept order and mandatory H1/H2 wording were aligned with the current mechanism-first guidance and optional H2/H3. CI previously checked seed coverage and smoke examples, not article generation. CI now runs deterministic evaluation-infrastructure tests without model credentials; no CI green result implies successful writing. The historical report remains unchanged.
