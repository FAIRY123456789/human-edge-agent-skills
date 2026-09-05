# Sanitized small-ECS baseline

This public baseline preserves reusable facts from a deployment verified in August 2026. It intentionally omits the address, SSH identity, application name, private routes, exact server paths, and all secret material.

| Item | Sanitized verified fact |
|---|---|
| Provider | Alibaba Cloud ECS |
| OS family | Alibaba Cloud Linux 3, x86_64 |
| Capacity class | 2 vCPU, about 2 GiB RAM, 40 GiB system disk, no swap at inspection time |
| Python finding | The system default was an old Python; the application used an explicit Python 3.11 interpreter and isolated virtual environment |
| Model compatibility | Serialized scikit-learn/joblib artifacts required an exact runtime compatibility check |
| Web topology | Nginx served static SPA assets and proxied a loopback API under an application subpath |
| Process model | One backend worker fit the memory budget better than unconstrained worker multiplication |
| Release model | Versioned release directories, shared state, atomic `current` symlink |
| Verified gates | Canary, production promotion, AI online/offline behavior, rollback, re-promotion, protected-site hashes, reboot recovery |
| Reusable risks | old system runtime, slow dependency index, directory execute bits, model-pickle drift, duplicate/default Nginx ownership, public-IP hairpin timeouts |

Use this as an example of the evidence to record, not as a recommended server specification. Measure the target host and current package requirements before selecting an image or instance.
