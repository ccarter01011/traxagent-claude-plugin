# Security

## What this plugin can reach

| Part | What it does | Network |
| --- | --- | --- |
| `ai-spend` MCP server | Read-only tools that return your company's AI spend from TraxAgent | `https://www.traxagent.io/mcp`, after you sign in with OAuth or a TraxAgent API token |
| `ai-spend-demo` MCP server | The same tools on a made-up company | `https://www.traxagent.io/mcp/demo`, no sign-in |
| `/spend-audit` command | Instructions for Claude to price your local Claude Code session logs in `~/.claude/projects` | None. No script ships with the plugin; you approve each step Claude takes |
| `ai-spend` and `spend-statusline` skills | Instructions for Claude | None of their own |

- Every MCP tool is read-only (`readOnlyHint: true`). None can change settings, keys, budgets or data.
- TraxAgent reads provider usage with read-only admin keys. It never sees prompts or model outputs, because the providers' usage and cost APIs don't return them.
- The plugin has no hooks and ships no scripts, binaries or dependencies: only Markdown, JSON and images.
- CI checks every push: manifests parse, versions match, the MCP servers are HTTPS on traxagent.io, and the plugin folder holds only Markdown, JSON and images, with no inline shell or pre-approved tools.

More on how TraxAgent handles data: https://www.traxagent.io/security

## Reporting a vulnerability

Email **support@traxagent.io** with "Security" in the subject, or use GitHub's private vulnerability reporting (Security tab, "Report a vulnerability"). Please don't open a public issue for a security problem.

We reply within 2 business days and tell you what we found and when a fix ships. We won't take legal action against good-faith research that avoids other people's data and doesn't disrupt the service.

## Supported versions

The latest release on `main` gets fixes. The MCP server is hosted, so server fixes reach every version at once.
