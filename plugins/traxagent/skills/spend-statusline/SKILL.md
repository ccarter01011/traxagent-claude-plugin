---
name: spend-statusline
description: Show session cost and Claude Code 5-hour and weekly limit use in the Claude Code status line. Use when the user wants to see what a session costs, how close they are to Claude Code limits, or their team's spend cap while they work.
---

# Spend in the status line

TraxAgent's free status line shows the model, this session's cost, and 5-hour and weekly limit use. With a TraxAgent account it also shows the person's spend cap and the day they'll reach it at their current pace.

1. Explain what it does and that the script only reads Claude Code's status-line input; with no account, nothing is sent anywhere.
2. With the user's OK, run:

   ```bash
   curl -fsSL https://www.traxagent.io/statusline/install.sh | bash
   ```

3. Tell them to restart Claude Code. The details are at https://www.traxagent.io/statusline.
