# Redacted server profile template

Create one profile per authorized host. Store it in the application repository only after redaction. Never add a public IP, hostname, username, credential, private route, private application name, database URL, token, or customer data to a public Skill repository.

| Item | Value |
|---|---|
| Profile date | YYYY-MM-DD |
| Provider / product | Alibaba Cloud ECS or compatible Linux VPS |
| Region class | broad geography only, if safe |
| OS image | distribution, release, architecture |
| Capacity | vCPU, RAM, swap, disk class and free space |
| Access | SSH alias or `<host>` placeholder; authentication method, never secret material |
| Python | absolute interpreter path and version, or not used |
| Node.js | binary path, version, package manager, or not used |
| Java | binary path, JRE major, or not used |
| Artifact runtime | libraries that affect serialized artifacts |
| Backend binding | loopback address and non-sensitive port placeholder |
| Public route | `<public-path>` or `<domain>` placeholder |
| App root | `/opt/<app>` |
| Releases | `/opt/<app>/releases/<version>` and atomic `current` |
| Shared state | `/opt/<app>/shared` or an explicitly documented external store |
| Environment | server-side file path; record only variable names and configured/empty status |
| Service | `<app>.service` |
| Nginx owner | discovered config path and owning server block, redacted if public |
| Backup root | `/opt/<app>-backups` or provider snapshot identifier |
| Protected sites | placeholder routes plus pre/post hash method |
| Known risks | evidence-backed environment risks and mitigations |
| Last verified | gate results, version checksum, and date |

Re-run remote preflight before every release. A profile is planning context, not proof of current state.
