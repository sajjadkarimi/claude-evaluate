---
description: Review a session and get tips (with estimated savings) to use fewer tokens
argument-hint: "[list | session number | transcript path]"
---

Use the efficiency-coach subagent to review how I used Claude and tell me how I could
have reduced my token consumption.

What to review, based on my argument: "$ARGUMENTS"

- empty: the current session
- "list": do not review anything; have the subagent list my recent sessions
- a number (as shown by "list"; 1 is the newest): that session
- a file path: that transcript

When the subagent finishes, show me its output as written. Do not add commentary,
re-run the analysis, or continue any earlier task.
