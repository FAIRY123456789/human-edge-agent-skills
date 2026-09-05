---
name: deployment-proof
description: Convert deployment logs, validation reports, Git history, and before/after notes into a redacted GitHub case study, portfolio entry, interview story, and evidence-backed resume bullets. Use after a software deployment, migration, recovery, or automation project when the user wants to demonstrate learning ability or impact without leaking host identities, credentials, private paths, customer data, or invented metrics. Do not publish or push unless the user explicitly asks.
---

# Deployment Proof

Turn operational work into credible public evidence. Preserve what was difficult, what changed, and how success was verified; remove everything that identifies or grants access to the system.

## Build an evidence ledger first

Collect only sources the user authorizes: deployment report, redacted logs, checksums, test output, Git diff/history, architecture notes, screenshots, and the original failure description. For each possible claim, record:

- claim;
- evidence source and date;
- baseline and result;
- verification method;
- confidentiality risk;
- confidence: confirmed, calculated, user-reported, or unknown.

Do not turn memory, confidence, or a successful health endpoint into a confirmed result. If the original process took “several days” but the automated run was not timed, say it became repeatable; do not invent a percentage or speedup.

## Redact before writing

Remove public IPs, hostnames, SSH usernames, private application names and routes, account IDs, exact private filesystem paths, credentials, tokens, database URLs, personal/customer data, and private questions or AI prompts. Preserve reusable environment facts such as OS family, architecture, capacity class, runtime major/minor, deployment topology, and failure class when safe.

Run:

```bash
python scripts/audit_public_report.py <draft-or-folder>
```

A clean scan is necessary but not sufficient. Manually review screenshots, Git history, document metadata, filenames, QR codes, terminal prompts, and contextual identifiers that regex cannot understand.

## Tell the problem-to-proof story

Copy [assets/case-study-template.md](assets/case-study-template.md) into the output project and fill only sections supported by evidence. Lead with the outcome and audience pain:

```text
Repeated manual deployment troubleshooting
-> reusable preflight/canary/promotion/rollback workflow
-> verified release plus a public, redacted evidence trail
```

Show a small architecture or gate sequence only when it makes the workflow easier to understand. Prefer a short verification table over a long command transcript.

## Produce reusable career assets

Create:

1. a concise GitHub case study;
2. three resume bullets using action, technical method, and demonstrated result;
3. a 60–90 second interview story covering problem, investigation, reusable system, verification, and learning;
4. a short launch post that invites feedback without claiming popularity;
5. a list of evidence still needed for stronger quantified claims.

Describe the Skill as an engineering artifact, not merely “using AI.” Emphasize problem discovery, workflow design, parameterization, safety boundaries, deterministic tooling, verification, iteration, and public documentation.

## Quality gate

Before delivery, confirm:

- every number has a source;
- every success claim names its verification;
- user-reported timing is labeled as such;
- the draft contains no secrets or private identifiers;
- compatibility scope matches what was actually tested;
- installation and first-use instructions are copyable;
- limitations and untested paths are visible;
- no publish, push, post, or external message occurred without explicit authorization.
