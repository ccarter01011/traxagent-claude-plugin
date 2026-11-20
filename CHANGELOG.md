# Changelog

## 1.4.1 (2026-11-20)
- `/spend-audit` is now plain instructions for Claude with the price table built in; the plugin no longer ships a Python script, inline shell or pre-approved tools.

## 1.4.0 (2026-11-20)
- New `get_ai_registry` tool: every AI tool, API key, coding agent and seat plan in use, with owner, approval status and what needs a look.
- Cursor plugin manifests moved to the same version as the Claude Code plugin.
- Added SECURITY.md, CONTRIBUTING.md, a code of conduct, issue templates and CI checks.

## 1.3.0 (2026-11-19)
- New `get_task_quality` tool: quality versus cost by task type, with a verdict on whether a cheaper model does the job.

## 1.2.0
- `get_people_spend`: AI spend per person across the API, Claude Code, Codex and Cursor.

## 1.1.2 (2026-11-18)
- Spend by person; works in ChatGPT and Cursor.
