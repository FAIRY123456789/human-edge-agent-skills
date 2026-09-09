# skills.sh Status

Snapshot: 2026-09-09 (Asia/Shanghai).

| Evidence | Current result |
|---|---|
| Pinned CLI checked | `skills` 1.5.25 |
| Discovery command | `npx --yes skills@1.5.25 add FAIRY123456789/human-edge-agent-skills --list` with `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` |
| Canonical Skills discovered by CLI | 18 |
| Skills indexed on directory page | 1: `vibe-to-spec` |
| Real total installs shown | 1 |
| Directory | https://skills.sh/fairy123456789/human-edge-agent-skills |
| Badge | https://skills.sh/b/fairy123456789/human-edge-agent-skills — HTTP 200, SVG |

The CLI emitted an engine warning because version 1.5.25 declares Node `>=22.20.0` while the host has Node 20.19.5, but the read-only list operation completed and found all 18 Skills. No Skill was installed by this check, so it did not manufacture telemetry or increase the public count.

## Security audit availability

The public audit API currently returns three passing partner results for the only indexed Skill, `vibe-to-spec`:

- Gen Agent Trust Hub: PASS, `SAFE`; notes a minor indirect-prompt-injection risk because the Skill processes untrusted transcript text.
- Socket: PASS, no alerts.
- Snyk: PASS, `LOW`, no issues.

Audit timestamps exposed by the API are 2026-09-05. A sampled URL for the unindexed `voice-dump-to-todo` returned HTTP 404. This report therefore does not generalize the three partner audits to all 18 Skills.

The official badge was added to the repository README because it points to the real repository-level count. The page remains partially indexed; the badge must not be read as evidence that all 18 Skills have directory listings or independent installs.

Official references:

- https://www.skills.sh/docs
- https://www.skills.sh/docs/cli
- https://www.skills.sh/docs/api
