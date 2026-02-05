# learn_bash_from_session_data

Learn bash from your Claude Code sessions. Extracts commands you've used, categorizes them, and generates an interactive HTML learning resource with quizzes.

## Installation

```bash
npm install -g learn_bash_from_session_data
```

## Usage

```bash
# Analyze all sessions from current project
learn-bash

# Analyze last 5 sessions
learn-bash -n 5

# List available projects
learn-bash --list

# Process specific session file
learn-bash --file ~/.claude/projects/.../session.jsonl

# Custom output path
learn-bash --output ./my-lessons.html
```

## Features

- **Command Extraction**: Parses Claude Code session JSONL files
- **Categorization**: Groups commands by category (Git, File System, Text Processing, etc.)
- **Complexity Scoring**: Rates commands from 1-5 based on complexity
- **Interactive Quizzes**: Test your knowledge with auto-generated quizzes
- **Self-Contained HTML**: No external dependencies, works offline

## Requirements

- Node.js >= 14.0.0
- Python >= 3.8

## License

MIT
