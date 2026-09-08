# deployment-proof

> **Turn invisible deployment work into credible public evidence**

Convert redacted deployment reports, validation output, Git history, and before/after notes into a GitHub case study, resume bullets, an interview story, and a launch post without inventing metrics or exposing infrastructure.

**Category:** Build in Public
**Keywords:** deployment, case-study, portfolio, resume, redaction, build-in-public, evidence

## Preview / install

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills deployment-proof
gh skill install FAIRY123456789/human-edge-agent-skills deployment-proof
```

## First prompt

```text
Use $deployment-proof to turn these deployment artifacts into a public case study and three resume bullets. Flag every unsupported metric and every item that may still identify the server.
```

Run `scripts/audit_public_report.py` on the draft, then manually inspect screenshots, filenames, Git history, and document metadata before publication.
