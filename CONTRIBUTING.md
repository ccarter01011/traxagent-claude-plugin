# Contributing

Thanks for helping. Issues and pull requests are welcome.

- **Bugs and ideas:** open an issue with the template. Say which client you use (Claude Code, Claude, ChatGPT, Cursor, VS Code) and what you asked.
- **Pull requests:** keep them small and say what changed and why. CI must pass (`python3 scripts/check.py` runs the same checks locally).
- **Versions:** bump `version` in every `plugin.json` together and add a line to `CHANGELOG.md`.
- **Security problems:** see [SECURITY.md](SECURITY.md) instead of opening an issue.

The plugin stays read-only: no tool that changes data, no hooks, and no network access from the local script.
