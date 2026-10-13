# claude-evaluate

`/efficiency-review` adds a token-efficiency coach to Claude Code.

Run it at the end of a session, or on a past one. A subagent reads the session
transcript, measures where tokens went, and writes a short review. It looks at:

- context growth
- cache hit ratio
- repeated file reads
- large tool results
- vague or corrected prompts
- plugins that might help, such as caveman or code-review-graph (suggested only when the session data supports it)

The review contains before-and-after rewrites of your own prompts, a few habits to
change, and a range of estimated savings.

Plain Python does the measuring, so the numbers are exact. Claude does the
interpreting. Savings are what-if estimates from the transcript, not measurements,
and the review reports what you would pay in tokens, not dollars.

## What's in the box

```
efficiency-review-command/.claude/
├── commands/efficiency-review.md  # the /efficiency-review slash command
├── agents/efficiency-coach.md     # subagent that interprets the numbers
└── scripts/session_stats.py       # measures a session transcript (Python 3, stdlib only)
```

`efficiency-review-command.zip` contains the same `.claude/` folder.

## Requirements

- Claude Code
- `python3` on your `PATH` (no third-party packages)

## Install

Pick one. Both copy the `.claude` folder so the command, agent and script sit together.

### Option A: all projects (user-level)

```bash
git clone https://github.com/sajjadkarimi/claude-evaluate.git
cd claude-evaluate
mkdir -p ~/.claude
cp -rn efficiency-review-command/.claude/* ~/.claude/
```

`-n` avoids overwriting existing files. The agent falls back to
`~/.claude/scripts/session_stats.py` when no project-level copy exists.

### Option B: one project only

From your project root:

```bash
cp -rn /path/to/claude-evaluate/efficiency-review-command/.claude/* .claude/
```

(Create `.claude/` first if it doesn't exist.) Commit it if you want teammates to get
the command too.

### Or from the zip

```bash
unzip efficiency-review-command.zip -d ~/        # user-level
unzip efficiency-review-command.zip -d .         # project-level
```

After installing, restart Claude Code (or start a new session) so it picks up the
command and agent. Check with `/agents`: `efficiency-coach` should be listed.

## Usage

| Command | What it does |
| --- | --- |
| `/efficiency-review` | Review the current (newest) session |
| `/efficiency-review list` | List recent sessions, newest = 1 |
| `/efficiency-review 3` | Review session number 3 from the list |
| `/efficiency-review path/to/transcript.jsonl` | Review a specific transcript file |

Typical flow: finish your work, run `/efficiency-review`, read the review, apply one or two
of the habits next session.

### Running the script directly

```bash
python3 .claude/scripts/session_stats.py             # newest session, JSON
python3 .claude/scripts/session_stats.py --list      # recent sessions
python3 .claude/scripts/session_stats.py --session 2
python3 .claude/scripts/session_stats.py path/to.jsonl
```

## Notes and limits

- Transcripts are read from `~/.claude/projects`. Claude Code deletes old sessions
  after its retention period, so very old sessions can't be reviewed.
- Tool-result sizes are estimated at about 4 characters per token.
- The transcript format is an internal detail of Claude Code and may change; if the
  script breaks after an update, the review will say so rather than invent numbers.
- Nothing is modified: the coach only reads transcripts.

## License

See [LICENSE](LICENSE).
