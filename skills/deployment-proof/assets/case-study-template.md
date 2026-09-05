# [Outcome-focused project title]

> [One sentence: audience, painful problem, and verifiable outcome.]

## The problem

[Describe the repeated failure, wasted effort, or risk. Separate observed facts from user-reported experience.]

## Why the obvious approach failed

[Explain the environment mismatch, missing evidence, routing/state issue, or unsafe release assumption.]

## The reusable system

```text
inspect -> preflight -> package -> canary -> promote -> verify -> roll back
```

[Explain only the decisions that materially changed reliability or speed.]

## Verification

| Gate | Status | Evidence |
|---|---|---|
| Local build/package | [PASS/FAIL/NOT TESTED] | [redacted command or artifact] |
| Canary | [PASS/FAIL/NOT TESTED] | [real flow checked] |
| Production | [PASS/FAIL/NOT TESTED] | [URL behavior, service, assets] |
| Rollback | [PASS/FAIL/NOT TESTED] | [version/state result] |
| Protected existing sites | [PASS/FAIL/NOT TESTED] | [pre/post comparison] |

## Before and after

| Before | After | Evidence quality |
|---|---|---|
| [baseline] | [result] | [confirmed/calculated/user-reported] |

## What I learned

[Connect technical findings to a new reusable decision rule.]

## Try it

```bash
[one installation command]
```

```text
[one realistic first prompt]
```

## Limits

[List untested runtimes, providers, scale, or flows.]
