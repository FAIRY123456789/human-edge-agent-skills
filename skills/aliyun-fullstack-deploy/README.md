# aliyun-fullstack-deploy

> **Canary-first deployment for small ECS and shared Linux servers**

Deploy React/Vue/Vite applications with Python, Node.js, or Java backends through evidence gates: inspect, package, canary, atomically promote, verify real flows, and roll back without sacrificing existing sites or persistent state.

**Category:** Engineering
**Keywords:** aliyun, ecs, linux-vps, nginx, systemd, canary, rollback, deployment

## Why it exists

A generic “deploy this project” prompt often discovers runtime drift, Nginx ownership, subpath errors, model incompatibility, or overwritten state only after production changes. This Skill makes those risks part of the deployment contract before mutation.

## Preview / install

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills aliyun-fullstack-deploy
gh skill install FAIRY123456789/human-edge-agent-skills aliyun-fullstack-deploy

# Or via the Skills CLI ecosystem
npx skills add https://github.com/FAIRY123456789/human-edge-agent-skills --skill aliyun-fullstack-deploy
```

## First prompt

```text
Use $aliyun-fullstack-deploy to inspect this app and my authorized ECS. Show the deployment contract and stop before the first remote mutation.
```

The bundled promotion/canary adapters are tested around a Python layout. Node.js and Java deployments use the same evidence contract but still require project-specific start commands and validation hooks.

This repository claims no external adoption yet. Review every script before use and test on a disposable target before production.
