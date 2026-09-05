# Runtime and instance selection

## Decision order

1. Read the repository's declared runtime, lockfiles, build target, model serializer versions, and native dependencies.
2. Check which compatible interpreters or runtimes the candidate OS image provides without replacing system-owned binaries.
3. Estimate peak build memory separately from steady-state runtime memory.
4. Prefer local or CI frontend builds when server RAM is limited; upload immutable outputs with checksums.
5. Reserve memory for the OS, Nginx, monitoring, SSH, package installation, and transient decompression before choosing worker count.
6. Choose the smallest instance that retains a safety margin under the measured workload. Do not infer production capacity from an idle process.

## Compatibility rules

- A recent server purchase date does not imply a recent default runtime. Verify the exact image release and binary paths.
- Python virtual environments isolate packages, not the interpreter ABI. Select the interpreter first, then create the environment.
- Java artifacts target a JRE major; verify it explicitly.
- Node native addons must match the server OS, architecture, Node ABI, and libc.
- Pickled or joblib model artifacts are deployment dependencies. Record the serializer and critical library versions or rebuild them in a controlled environment.

## Capacity evidence

Record idle and exercised RSS, disk use before and after dependencies, build peak memory, response latency for a representative flow, and restart behavior. If these are not measured, report capacity as `NOT TESTED` rather than “sufficient.”
