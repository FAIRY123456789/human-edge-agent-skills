# small-server-fit

> **Know whether the app fits before buying or deploying the server**

Compare an application's measured build/runtime budget with a low-cost VPS or Alibaba Cloud ECS, then report `FIT`, `FIT WITH CHANGES`, `NOT FIT`, or `NOT MEASURED` without guessing capacity.

**Category:** Engineering
**Keywords:** ecs, vps, capacity-planning, python, nodejs, java, memory, deployment

## Preview / install

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills small-server-fit
gh skill install FAIRY123456789/human-edge-agent-skills small-server-fit

# Or via the Skills CLI ecosystem
npx skills add https://github.com/FAIRY123456789/human-edge-agent-skills --skill small-server-fit
```

## First prompt

```text
Use $small-server-fit to assess whether this repository fits a 2 vCPU / 2 GiB Linux VPS. Separate verified facts from missing measurements and do not purchase anything.
```

The included calculator performs arithmetic only from explicit measurements; it does not convert idle memory or marketing specifications into a production-capacity claim.
