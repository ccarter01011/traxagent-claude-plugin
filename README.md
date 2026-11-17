# TraxAgent for Claude Code

**Who spent your AI budget last month, and on what?** Ask Claude, and get the answer from your real usage.

Your teams probably pay for AI in five places: the Anthropic, OpenAI and Gemini APIs, Claude Code or Codex, Cursor, and Claude or ChatGPT seats. Each vendor's console is correct about its own slice and blind to the rest.

[TraxAgent](https://www.traxagent.io/?ref=github-plugin) pulls them into one place every night, by team and by person. Then an AI review goes through your usage and tells you where you're overpaying. Each fix comes with what it costs you per month and the exact change to make. You walk into the budget meeting with the full number, where it went, and what you've already done to bring it down.

This plugin puts all of that inside Claude Code.

## What you can do from Claude Code

- **Ask about spend in plain English.** "What did we spend on AI last week, by team?" "Which API key is using the most Opus?" "Why did spend jump on Tuesday?"
- **Ship the fixes.** "What's the biggest cost fix, and can you ship it here?" Claude pulls the fix's steps from TraxAgent, makes the change in your repo and opens a pull request that states the monthly saving.
- **See spend while you work.** The spend status line shows this session's cost, your 5-hour and weekly Claude Code limit use, and, with an account, your spend cap and the day you'll reach it at your current pace.

Example answer, from a real account:

```
AI spend, Nov 10–16: $26.89 total (about $3.84/day, list prices)

| Team                 | Spend  |
|----------------------|--------|
| TraxAgent (internal) | $26.73 |
| Unlabeled            | $0.10  |
| Data science         | $0.06  |

Biggest open cost fix: none right now.
```

## Install

In Claude Code:

```
/plugin marketplace add ccarter01011/traxagent-claude-plugin
/plugin install traxagent@traxagent
```

Then run `/mcp`, pick `plugin:traxagent:ai-spend`, choose **Authenticate** and sign in to TraxAgent in your browser. There's no token to copy. The MCP server is on TraxAgent's paid plans.

No account yet? [Set one up in about 5 minutes](https://www.traxagent.io/setup?ref=github-plugin) by pasting a read-only admin key. TraxAgent is free up to $100 a month of AI spend.

## Look first, no sign-up (about 2 minutes each)

1. [Free audit](https://www.traxagent.io/audit?ref=github-plugin): upload a usage CSV, no admin key needed. You get the findings on the spot, each with its monthly cost and the exact fix.
2. [Speed Index](https://www.traxagent.io/speed?ref=github-plugin): race your own prompt across 10 Claude and OpenAI models.
3. [Demo](https://www.traxagent.io/demo?ref=github-plugin): see the whole product on sample data.

## Spend caps

Some companies now cap each engineer's AI spend by day, week or month. If leadership asks whether your teams need one, test a cap against your own numbers before you set it. TraxAgent shows who would hit it and how often, then warns people early, before they reach it, and again at 80% and 100%.

## Trust and security

- **Read-only.** TraxAgent reads usage reports with read-only admin keys. Neither the keys nor this plugin can change anything at your providers.
- **No prompts or outputs.** TraxAgent never receives what you send to models, only usage and cost.
- **OAuth sign-in.** The plugin connects with OAuth 2.1 (PKCE), using short-lived tokens. You can disconnect any app under **API and MCP → Connected apps**.
- **Open plugin.** Everything this plugin does is in this repo: one MCP server address and two skills.

More detail: [Security](https://www.traxagent.io/security?ref=github-plugin) · [Privacy](https://www.traxagent.io/privacy?ref=github-plugin) · [How it works](https://www.traxagent.io/integrations?ref=github-plugin)

## What's in this plugin

| Part | What it does |
|---|---|
| `ai-spend` MCP server | Read-only tools: `get_spend_summary`, `get_spend`, `list_fixes`, `get_fix_prompt`, `list_api_keys` |
| `ai-spend` skill | Tells Claude how to answer spend questions and ship fixes as pull requests |
| `spend-statusline` skill | Installs the TraxAgent status line, with your OK |

## License

MIT. Questions: [traxagent.io](https://www.traxagent.io/?ref=github-plugin)
