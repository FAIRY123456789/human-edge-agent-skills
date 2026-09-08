# Privacy and data handling

Last updated: 2026-09-08

This plugin is a local instruction package. The publisher operates no service for it and does not collect telemetry, analytics, account information, prompts, transcripts, generated content, or usage data.

The plugin does not send content to a publisher-controlled endpoint. Any processing performed by the host is governed by that host's own terms and privacy controls. Users should remove secrets, private names, and confidential information before providing transcripts to a host.

The bundled render_todo.py helper reads a user-provided JSON file and writes an HTML file at a path chosen by the user. It has no network calls, telemetry, credential access, or background execution.

The plugin declares no MCP servers, hooks, commands, agents, rules, environment variables, secret access, or automatic permissions. It stores only files the user explicitly asks the host or helper to create locally.

Privacy questions and security reports may be opened through the repository's GitHub Issues page.
