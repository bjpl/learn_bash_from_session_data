# learn_bash_from_session_data

Turn your Claude Code sessions into personalized bash lessons. This tool extracts every command you've run, enriches them with descriptions and flag breakdowns from a 402-command knowledge base, generates interactive quizzes, and produces a self-contained HTML learning resource.

## Installation

```bash
npm install -g learn_bash_from_session_data
```

**Requirements:** Node.js >= 14.0.0 and Python >= 3.8

## Quick Start

```bash
# Generate a lesson from your current project's sessions
learn-bash

# Process the last 5 sessions only
learn-bash -n 5

# List all available Claude Code projects
learn-bash --list
```

The generated HTML opens automatically in your browser.

## CLI Reference

```
learn-bash [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--sessions <count>` | `-n` | Number of recent sessions to process (default: all) |
| `--file <path>` | `-f` | Process a specific session JSONL file |
| `--output <path>` | `-o` | Output directory path (default: `./bash-learner-output/`) |
| `--project <name>` | `-p` | Process sessions from a specific project by name |
| `--list` | `-l` | List available Claude Code projects with session counts |
| `--no-open` | | Don't auto-open the generated HTML in browser |
| `--help` | `-h` | Show help message |

### Examples

```bash
# Process a specific session file
learn-bash --file ~/.claude/projects/my-project/abc123.jsonl

# Output to a custom location without opening browser
learn-bash -o ./my-lessons --no-open

# Process sessions from a named project
learn-bash --project "C--Users-me-my-app"

# Process last 3 sessions, custom output
learn-bash -n 3 -o ./review
```

## What You Get

The tool generates a single interactive HTML file with four sections:

### Commands Tab
Every bash command you used, organized by category with:
- Syntax-highlighted full command display
- Flag breakdowns with descriptions (e.g., `-l` = "Long format listing with permissions, size, dates")
- Subcommand explanations (e.g., `git add` = "Stage file contents for commit")
- Common usage patterns from the knowledge base
- Search, sort (by frequency, complexity, category, name), and category filtering

### Lessons Tab
Step-by-step walkthrough of commands grouped by category, with flag details and complexity indicators. Designed for sequential learning.

### Quiz Tab
20 auto-generated questions in four types:

| Type | Weight | What It Tests |
|------|--------|---------------|
| What does this do? | 40% | Identify a command's purpose from its syntax |
| Which flag? | 25% | Match a flag to its behavior |
| Build the command | 20% | Construct the correct command for a task |
| Spot the difference | 15% | Compare two similar commands |

Quizzes are **session-adaptive** (based on commands you actually used), **randomized** (different questions and answer order each run), and use plausible distractors drawn from 402 real commands.

### Summary Tab
Statistics on your session: total commands, category distribution, complexity breakdown, most-used commands.

## Knowledge Base

The built-in knowledge base powers descriptions, flag lookups, and quiz generation:

| Metric | Count |
|--------|-------|
| Commands documented | 402 |
| Flag definitions | 1,961 |
| Common usage patterns | 1,357 |
| Categories | 11 |
| Bash operators | 16 |
| Bash concepts | 6 |

### Categories

File System, Text Processing, Git, Package Management, Process & System, Networking, Permissions, Compression, Search & Navigation, Development, Shell Builtins

## How It Works

```
Claude Code session (.jsonl)
    |
    v
[Parser] --> Extract bash tool_use blocks
    |
    v
[Extractor] --> Split compound commands (pipes, &&, ;)
    |
    v
[Analyzer] --> Categorize, score complexity (1-5), count frequency
    |
    v
[Knowledge Base] --> Enrich with 402 commands, 1961 flags, 1357 patterns
    |
    v
[Quiz Generator] --> 20 randomized, session-adaptive questions
    |
    v
[HTML Generator] --> Self-contained interactive HTML (no dependencies)
```

## Session File Location

Claude Code stores sessions at:

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.claude/projects/` |
| Windows | `%USERPROFILE%\.claude\projects\` |
| WSL | Auto-detected from `/mnt/c/Users/<name>/.claude/projects/` |

Each project directory contains `.jsonl` session files that this tool reads.

## Programmatic Usage

You can also run the Python pipeline directly:

```bash
python scripts/main.py --sessions 5 --output ./output
```

Or import modules in Python:

```python
from scripts.knowledge_base import COMMAND_DB, get_flags_for_command, get_command_info
from scripts.quiz_generator import generate_quiz_set
from scripts.analyzer import analyze_commands

# Look up a command
info = get_command_info("grep")
flags = get_flags_for_command("grep")

# Generate quizzes from analyzed commands
quizzes = generate_quiz_set(analyzed_commands, count=10)
```

## License

MIT
