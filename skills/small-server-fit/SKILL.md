---
name: small-server-fit
description: Assess whether a web application and its build/runtime plan fit a low-cost Linux VPS or Alibaba Cloud ECS before purchase, implementation, or deployment. Use when choosing an OS image, Python/Node/Java versions, build location, worker count, swap strategy, or minimum CPU/RAM/disk for a repository. Produce evidence-backed FIT, FIT WITH CHANGES, NOT FIT, or NOT MEASURED decisions; do not recommend purchasing from guessed capacity.
---

# Small Server Fit

Prevent avoidable deployment rework by checking application requirements against a measured server budget before committing to an image, runtime, or instance size.

## Establish the two sides of the fit

Inspect the repository for:

- frontend build tool and whether static assets can be built locally or in CI;
- backend runtime and exact version constraints;
- lockfiles, native extensions, browser binaries, ML/model artifacts, and serializer versions;
- steady processes, intended worker count, background jobs, databases, uploads, logs, and temporary build space;
- representative validation flow and concurrency expectation.

Obtain a current or candidate server profile containing OS image, architecture, vCPU, RAM, swap, disk and free space, available runtime versions, and platform services. Use [references/profile-schema.md](references/profile-schema.md) for the evidence contract.

If the host does not exist yet, mark runtime measurements `NOT MEASURED` and separate image compatibility from capacity claims. Do not treat a purchase date or marketing label as proof of installed runtime versions.

## Make the fit decisions

Evaluate these independently:

1. **OS/architecture fit:** application binaries and native packages support the image and architecture.
2. **Runtime fit:** an application-specific Python, Node.js, or Java runtime can be installed without replacing a system-owned runtime.
3. **Build fit:** peak dependency installation and build memory/disk fit, or the build can move to local/CI.
4. **Runtime memory fit:** measured or bounded steady processes leave headroom for the OS, Nginx, SSH, logs, and short spikes.
5. **Persistence fit:** state is outside immutable release directories and backups fit the disk or an external store.
6. **Operations fit:** the service can restart, recover after reboot, expose only intended ports, and produce bounded logs.

Run `scripts/evaluate_fit.py --profile <profile.json>` when numeric evidence is available. The script calculates margins; it does not invent missing workload measurements.

## Prefer changes in this order

1. Build the SPA or Java artifact outside the small server.
2. Isolate the application runtime instead of upgrading system binaries.
3. Reduce process/worker count when the workload and state model permit it.
4. Move databases, object storage, or heavy build jobs to a managed/external service when justified.
5. Add swap only as a bounded resilience measure, not as a substitute for required RAM.
6. Increase the instance size when measured steady-state plus safety margin still does not fit.

Never recommend downgrading security, removing backups, disabling verification, or co-locating incompatible state merely to claim fit.

## Output

Report each dimension as `FIT`, `FIT WITH CHANGES`, `NOT FIT`, or `NOT MEASURED`. Include:

- the recommended OS image and runtime isolation method;
- local/CI versus server build split;
- process and worker budget;
- RAM and disk arithmetic with source measurements;
- model/native dependency compatibility risks;
- the smallest safe next measurement or experiment;
- a purchase recommendation only when evidence supports it.

Distinguish a confirmed fact, calculation, assumption, and recommendation. A useful result can be `NOT MEASURED`; false precision cannot.
