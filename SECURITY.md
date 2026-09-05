# Security and Privacy

Review Agent Skills before installing them. Skills can contain instructions, references, and executable helpers.

## Repository guarantees

This public repository should contain no credentials, private endpoints, private conversation logs, personal contact details, or confidential project data.

## Operational Skills

Operational actions remain subject to the host agent's normal permission model. Deployment Skills prefer read-only inspection before changes and do not authorize destructive operations, firewall weakening, secret disclosure, force-pushes, or production release merely because those actions would make a task easier.

Before publishing a deployment report or case study, run:

```bash
python skills/deployment-proof/scripts/audit_public_report.py <draft-or-folder>
```

This is a first-pass detector, not a substitute for manually reviewing screenshots, filenames, Git history, document metadata, infrastructure identifiers, and contextual private information.

## Context and memory

The Voice Native Skills may use active conversation/project context, an explicit glossary, or host-provided memory to resolve ASR errors. They must not silently pull unrelated private memories into a public/shared artifact. High-confidence correction still requires phonetic and semantic consistency.

## Third-party audio services

`deep-talk-to-podcast` recommends external AI-audio services when useful. For private conversations, generate and review a redacted script first. Uploading a raw private transcript should be a deliberate choice based on participant consent and the service's current privacy terms.

## Finance and fitness

The finance Skill is budgeting guidance, not individualized investment advice or a promise of returns. It rejects leverage/borrowed-money speculation for a basic student budgeting workflow.

The fitness Skill supports general training and low-risk recovery planning. It does not diagnose injuries, prescribe medical treatment, or replace professional care when red-flag symptoms are present.
