#!/usr/bin/env python3
"""
Quiz Generator for Bash Learning System

Generates quizzes from analyzed session commands with 4 question types:
1. "What does this do?" - Multiple choice about command behavior
2. "Which flag?" - Identify correct flag for a task
3. "Build the command" - Arrange components to form command
4. "Spot the difference" - Explain difference between similar commands

Uses ONLY Python standard library.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import random
import re
import hashlib

try:
    from scripts.knowledge_base import COMMAND_DB, get_command_info, get_flags_for_command
except ImportError:
    try:
        from knowledge_base import COMMAND_DB, get_command_info, get_flags_for_command
    except ImportError:
        COMMAND_DB = {}
        def get_command_info(name): return None
        def get_flags_for_command(command): return {}


def _get_flags_for_cmd(cmd: str) -> dict[str, str]:
    """Get merged flags for a command from knowledge_base (primary) and local FLAG_DATABASE (fallback).

    Knowledge_base.py COMMAND_DB is the authoritative source. FLAG_DATABASE provides
    additional coverage for commands not yet in knowledge_base.
    """
    flags = {}
    # Primary source: knowledge_base COMMAND_DB
    kb_flags = get_flags_for_command(cmd)
    if kb_flags:
        flags.update(kb_flags)
    # Fallback/supplement: local FLAG_DATABASE
    if cmd in FLAG_DATABASE:
        for flag, desc in FLAG_DATABASE[cmd].items():
            if flag not in flags:
                flags[flag] = desc
    return flags


def _get_all_flagged_commands() -> set[str]:
    """Get the set of all commands that have flag data from any source."""
    cmds = set()
    for cmd, info in COMMAND_DB.items():
        if info.get("flags"):
            cmds.add(cmd)
    cmds.update(FLAG_DATABASE.keys())
    return cmds


class QuizType(Enum):
    """Types of quiz questions."""
    WHAT_DOES = "what_does_this_do"
    WHICH_FLAG = "which_flag"
    BUILD_COMMAND = "build_the_command"
    SPOT_DIFFERENCE = "spot_the_difference"


@dataclass
class QuizOption:
    """A single quiz answer option."""
    id: str
    text: str
    is_correct: bool
    explanation: Optional[str] = None


@dataclass
class QuizQuestion:
    """A complete quiz question with options."""
    id: str
    quiz_type: QuizType
    question_text: str
    options: list[QuizOption]
    correct_option_id: str
    explanation: str
    difficulty: int  # 1-5
    command_context: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "type": self.quiz_type.value,
            "question": self.question_text,
            "options": [
                {
                    "id": opt.id,
                    "text": opt.text,
                    "is_correct": opt.is_correct,
                    "explanation": opt.explanation
                }
                for opt in self.options
            ],
            "correct_answer": self.correct_option_id,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
            "command_context": self.command_context,
            "tags": self.tags
        }


@dataclass
class Quiz:
    """A complete quiz containing multiple questions."""
    id: str
    title: str
    description: str
    questions: list[QuizQuestion]
    total_points: int = 0
    time_limit_seconds: Optional[int] = None

    def __post_init__(self):
        if self.total_points == 0:
            self.total_points = len(self.questions)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "questions": [q.to_dict() for q in self.questions],
            "total_points": self.total_points,
            "time_limit_seconds": self.time_limit_seconds,
            "question_count": len(self.questions)
        }


# =============================================================================
# Flag Knowledge Base (embedded for standalone use)
# =============================================================================

FLAG_DATABASE: dict[str, dict[str, str]] = {
    "ls": {
        "-l": "Use long listing format with details",
        "-a": "Show all files including hidden ones",
        "-h": "Human-readable file sizes",
        "-R": "List subdirectories recursively",
        "-t": "Sort by modification time",
        "-S": "Sort by file size",
        "-r": "Reverse sort order",
        "-1": "List one file per line",
        "-d": "List directories themselves, not contents",
        "-i": "Show inode numbers"
    },
    "grep": {
        "-i": "Case-insensitive search",
        "-r": "Search recursively in directories",
        "-n": "Show line numbers",
        "-v": "Invert match (show non-matching lines)",
        "-c": "Count matching lines only",
        "-l": "Show only filenames with matches",
        "-w": "Match whole words only",
        "-E": "Use extended regular expressions",
        "-A": "Show lines after match",
        "-B": "Show lines before match",
        "-C": "Show context lines around match",
        "-o": "Show only the matching part",
        "-q": "Quiet mode, exit status only"
    },
    "find": {
        "-name": "Search by filename pattern",
        "-type": "Filter by file type (f=file, d=directory)",
        "-size": "Filter by file size",
        "-mtime": "Filter by modification time",
        "-exec": "Execute command on found files",
        "-delete": "Delete found files",
        "-maxdepth": "Limit search depth",
        "-mindepth": "Minimum search depth",
        "-perm": "Filter by permissions",
        "-user": "Filter by owner",
        "-group": "Filter by group",
        "-newer": "Find files newer than reference"
    },
    "chmod": {
        "-R": "Change permissions recursively",
        "-v": "Verbose output",
        "-c": "Report only when changes made",
        "-f": "Suppress error messages",
        "--reference": "Use another file's permissions"
    },
    "cp": {
        "-r": "Copy directories recursively",
        "-i": "Prompt before overwriting",
        "-f": "Force overwrite without prompting",
        "-v": "Verbose output",
        "-p": "Preserve file attributes",
        "-a": "Archive mode (preserve all)",
        "-n": "Do not overwrite existing files",
        "-u": "Update only (copy if source is newer)",
        "-l": "Create hard links instead of copying",
        "-s": "Create symbolic links instead"
    },
    "mv": {
        "-i": "Prompt before overwriting",
        "-f": "Force overwrite without prompting",
        "-v": "Verbose output",
        "-n": "Do not overwrite existing files",
        "-u": "Update only (move if source is newer)",
        "-b": "Create backup of existing files"
    },
    "rm": {
        "-r": "Remove directories recursively",
        "-f": "Force removal without prompting",
        "-i": "Prompt before each removal",
        "-v": "Verbose output",
        "-d": "Remove empty directories"
    },
    "mkdir": {
        "-p": "Create parent directories as needed",
        "-v": "Verbose output",
        "-m": "Set permissions mode"
    },
    "cat": {
        "-n": "Number all output lines",
        "-b": "Number non-blank lines only",
        "-s": "Squeeze multiple blank lines",
        "-A": "Show all non-printing characters",
        "-E": "Show $ at end of each line",
        "-T": "Show tabs as ^I"
    },
    "tar": {
        "-c": "Create a new archive",
        "-x": "Extract files from archive",
        "-v": "Verbose output",
        "-f": "Specify archive filename",
        "-z": "Compress with gzip",
        "-j": "Compress with bzip2",
        "-t": "List archive contents",
        "-r": "Append files to archive",
        "-u": "Update files in archive",
        "--exclude": "Exclude files matching pattern"
    },
    "curl": {
        "-o": "Write output to file",
        "-O": "Save with remote filename",
        "-L": "Follow redirects",
        "-s": "Silent mode",
        "-v": "Verbose output",
        "-H": "Add custom header",
        "-X": "Specify HTTP method",
        "-d": "Send POST data",
        "-I": "Fetch headers only",
        "-k": "Allow insecure SSL connections",
        "-u": "Specify username:password",
        "-A": "Set User-Agent string"
    },
    "wget": {
        "-O": "Write to specified file",
        "-q": "Quiet mode",
        "-v": "Verbose output",
        "-c": "Continue partial download",
        "-r": "Recursive download",
        "-np": "Don't ascend to parent directory",
        "-P": "Specify download directory",
        "-N": "Only download newer files"
    },
    "git": {
        "--amend": "Amend the previous commit",
        "-m": "Specify commit message",
        "-a": "Stage all modified files",
        "-b": "Create and checkout new branch",
        "-f": "Force operation",
        "-v": "Verbose output",
        "--hard": "Reset working directory and index",
        "--soft": "Reset only HEAD",
        "-u": "Set upstream tracking branch"
    },
    "ssh": {
        "-p": "Specify port number",
        "-i": "Specify identity file",
        "-v": "Verbose mode",
        "-X": "Enable X11 forwarding",
        "-L": "Local port forwarding",
        "-R": "Remote port forwarding",
        "-N": "No remote command",
        "-f": "Go to background"
    },
    "scp": {
        "-r": "Copy directories recursively",
        "-P": "Specify port number",
        "-i": "Specify identity file",
        "-v": "Verbose mode",
        "-C": "Enable compression",
        "-p": "Preserve file attributes"
    },
    "ps": {
        "-e": "Show all processes",
        "-f": "Full format listing",
        "-u": "Show user-oriented format",
        "-a": "Show processes for all users",
        "-x": "Show processes without controlling terminal",
        "aux": "Common combination for all processes"
    },
    "kill": {
        "-9": "Force kill (SIGKILL)",
        "-15": "Graceful termination (SIGTERM)",
        "-l": "List all signal names",
        "-s": "Specify signal by name"
    },
    "awk": {
        "-F": "Specify field separator",
        "-v": "Set variable",
        "-f": "Read program from file"
    },
    "sed": {
        "-i": "Edit files in place",
        "-e": "Add script command",
        "-n": "Suppress automatic printing",
        "-r": "Use extended regular expressions",
        "-E": "Use extended regular expressions (portable)"
    },
    "sort": {
        "-n": "Sort numerically",
        "-r": "Reverse sort order",
        "-k": "Sort by specific field",
        "-u": "Remove duplicates",
        "-t": "Specify field delimiter",
        "-h": "Human numeric sort"
    },
    "uniq": {
        "-c": "Prefix lines with occurrence count",
        "-d": "Only print duplicate lines",
        "-u": "Only print unique lines",
        "-i": "Ignore case differences"
    },
    "head": {
        "-n": "Specify number of lines",
        "-c": "Specify number of bytes"
    },
    "tail": {
        "-n": "Specify number of lines",
        "-f": "Follow file (watch for appends)",
        "-c": "Specify number of bytes"
    },
    "wc": {
        "-l": "Count lines",
        "-w": "Count words",
        "-c": "Count bytes",
        "-m": "Count characters"
    },
    "diff": {
        "-u": "Unified diff format",
        "-r": "Recursively compare directories",
        "-q": "Only report if files differ",
        "-i": "Ignore case differences",
        "-w": "Ignore whitespace",
        "-B": "Ignore blank lines"
    },
    "du": {
        "-h": "Human-readable sizes",
        "-s": "Display only total for each argument",
        "-a": "Include files, not just directories",
        "-c": "Produce grand total",
        "-d": "Max depth to display"
    },
    "df": {
        "-h": "Human-readable sizes",
        "-T": "Show filesystem type",
        "-i": "Show inode information"
    },
    "chmod": {
        "-R": "Change permissions recursively",
        "-v": "Verbose output"
    },
    "chown": {
        "-R": "Change ownership recursively",
        "-v": "Verbose output",
        "-h": "Affect symbolic links"
    }
}

# Command categories for generating related distractors
COMMAND_CATEGORIES: dict[str, list[str]] = {
    "file_listing": ["ls", "find", "locate", "tree", "stat"],
    "file_manipulation": ["cp", "mv", "rm", "mkdir", "rmdir", "touch"],
    "text_processing": ["grep", "sed", "awk", "cut", "sort", "uniq", "tr"],
    "text_viewing": ["cat", "less", "more", "head", "tail", "wc"],
    "archiving": ["tar", "zip", "unzip", "gzip", "gunzip", "bzip2"],
    "networking": ["curl", "wget", "ssh", "scp", "rsync", "ping", "netstat"],
    "process_management": ["ps", "kill", "top", "htop", "jobs", "bg", "fg"],
    "version_control": ["git"],
    "permissions": ["chmod", "chown", "chgrp"],
    "disk_usage": ["du", "df", "mount", "umount"],
    "comparison": ["diff", "cmp", "comm"]
}

# Common flag descriptions that can be swapped as distractors
COMMON_FLAG_DESCRIPTIONS: dict[str, list[str]] = {
    "-v": ["Verbose output", "Version information", "Validate input"],
    "-r": ["Recursive operation", "Reverse order", "Read-only mode"],
    "-f": ["Force operation", "File input", "Format output"],
    "-n": ["Numeric output", "No newline", "Number lines", "Dry run"],
    "-i": ["Interactive mode", "Case-insensitive", "In-place edit"],
    "-a": ["All items", "Append mode", "Archive mode"],
    "-l": ["Long format", "List only", "Line mode"],
    "-h": ["Human-readable", "Help message", "Show hidden"]
}


def _generate_id(content: str) -> str:
    """Generate a unique ID based on content."""
    return hashlib.md5(content.encode()).hexdigest()[:8]


def _get_command_category(cmd: str) -> Optional[str]:
    """Get the category of a command."""
    for category, commands in COMMAND_CATEGORIES.items():
        if cmd in commands:
            return category
    return None


def _get_related_commands(cmd: str) -> list[str]:
    """Get commands in the same category."""
    category = _get_command_category(cmd)
    if category:
        return [c for c in COMMAND_CATEGORIES[category] if c != cmd]
    return []


def _generate_bash_description(cmd_string: str) -> str:
    """
    Generate an educational description focusing on bash concepts.

    Explains what each part of the command does from a bash perspective.
    Handles: &&, ||, |, 2>&1, 2>/dev/null, and combinations.
    """
    if not cmd_string:
        return "Runs a command"

    # Clean up redirections for description (note them but don't clutter)
    has_stderr_to_stdout = '2>&1' in cmd_string
    has_stderr_to_null = '2>/dev/null' in cmd_string
    has_stdout_redirect = re.search(r'>\s*\S+', cmd_string) and '2>' not in cmd_string

    # Remove redirections for parsing (we'll note them separately)
    clean_cmd = re.sub(r'\s*2>&1\s*', ' ', cmd_string)
    clean_cmd = re.sub(r'\s*2>/dev/null\s*', ' ', clean_cmd)
    clean_cmd = re.sub(r'\s*>\s*\S+\s*', ' ', clean_cmd)
    clean_cmd = ' '.join(clean_cmd.split())  # normalize whitespace

    parts = []

    # Handle && (run if previous succeeds)
    if ' && ' in clean_cmd:
        commands = clean_cmd.split(' && ')
        for i, cmd in enumerate(commands):
            cmd = cmd.strip()
            if not cmd:
                continue
            # Handle nested || or | within && segments
            if ' || ' in cmd:
                parts.append(_describe_or_chain(cmd))
            elif ' | ' in cmd:
                parts.append(_describe_pipe_chain(cmd))
            elif i == 0:
                parts.append(_describe_single_command(cmd))
            else:
                parts.append(f"then {_describe_single_command(cmd)}")

    # Handle || (run if previous fails)
    elif ' || ' in clean_cmd:
        parts.append(_describe_or_chain(clean_cmd))

    # Handle | (pipe)
    elif ' | ' in clean_cmd:
        parts.append(_describe_pipe_chain(clean_cmd))

    else:
        parts.append(_describe_single_command(clean_cmd))

    result = ', '.join(parts)

    # Add redirection notes
    if has_stderr_to_null:
        result += " (suppressing errors)"
    elif has_stderr_to_stdout:
        result += " (capturing all output)"

    return result


def _describe_or_chain(cmd_string: str) -> str:
    """Describe an || chain (fallback pattern)."""
    commands = cmd_string.split(' || ')
    parts = []
    for i, cmd in enumerate(commands):
        cmd = cmd.strip()
        if not cmd:
            continue
        # Handle pipes within || segments
        if ' | ' in cmd:
            desc = _describe_pipe_chain(cmd)
        else:
            desc = _describe_single_command(cmd)

        if i == 0:
            parts.append(desc)
        else:
            parts.append(f"or if that fails, {desc}")
    return ', '.join(parts)


def _describe_pipe_chain(cmd_string: str) -> str:
    """Describe a pipe chain."""
    commands = cmd_string.split(' | ')
    parts = []
    for i, cmd in enumerate(commands):
        cmd = cmd.strip()
        if not cmd:
            continue
        desc = _describe_single_command(cmd)
        if i == 0:
            parts.append(desc)
        else:
            parts.append(f"pipes to {desc}")
    return ', '.join(parts)


def _describe_single_command(cmd: str) -> str:
    """Generate description for a single command (no pipes/chains)."""
    if not cmd:
        return "runs a command"

    tokens = cmd.split()
    base_cmd = tokens[0] if tokens else ''

    # Get args (skip flags) for knowledge_base fallback
    args = [t for t in tokens[1:] if not t.startswith('-')]

    # Check knowledge_base COMMAND_DB for rich description
    if base_cmd and base_cmd in COMMAND_DB:
        cmd_info = COMMAND_DB[base_cmd]
        kb_desc = cmd_info.get('description', '')
        if kb_desc:
            # Use knowledge base description but make it contextual with args
            if args:
                return f"{kb_desc.lower()} ({' '.join(args[:2])})"
            return kb_desc.lower()

    # Common command descriptions with bash focus
    descriptions = {
        'cd': lambda args: f"changes directory to {args[0] if args else 'specified path'}",
        'ls': lambda args: f"lists {'files in ' + args[0] if args else 'directory contents'}",
        'mkdir': lambda args: f"creates directory {args[0] if args else ''}",
        'rm': lambda args: f"removes {args[0] if args else 'files'}",
        'cp': lambda args: f"copies files{' to ' + args[-1] if len(args) > 1 else ''}",
        'mv': lambda args: f"moves/renames files{' to ' + args[-1] if len(args) > 1 else ''}",
        'cat': lambda args: f"displays contents of {args[0] if args else 'file'}",
        'echo': lambda args: f"prints {'text' if not args else repr(' '.join(args)[:30])}",
        'grep': lambda args: f"searches for pattern in {'files' if len(args) > 1 else 'input'}",
        'find': lambda args: f"finds files{' in ' + args[0] if args else ''} matching criteria",
        'git': lambda args: f"runs git {args[0] if args else 'command'}" + _describe_git_subcommand(args),
        'python': lambda args: "executes Python script" + (' from heredoc' if '<<' in cmd else ''),
        'python3': lambda args: "executes Python 3 script" + (' from heredoc' if '<<' in cmd else ''),
        'npm': lambda args: f"runs npm {args[0] if args else 'command'}",
        'pip': lambda args: f"runs pip {args[0] if args else 'command'}",
        'docker': lambda args: f"runs docker {args[0] if args else 'command'}",
        'chmod': lambda args: f"changes permissions{' to ' + args[0] if args else ''}",
        'chown': lambda args: "changes file ownership",
        'curl': lambda args: "fetches URL content",
        'wget': lambda args: "downloads file from URL",
        'tar': lambda args: "archives/extracts tar files",
        'ssh': lambda args: f"connects via SSH{' to ' + args[0] if args else ''}",
        'sudo': lambda args: f"runs as superuser: {_describe_single_command(' '.join(args))}",
        'export': lambda args: f"sets environment variable {args[0].split('=')[0] if args else ''}",
        'source': lambda args: f"loads {args[0] if args else 'script'} into current shell",
        '.': lambda args: f"loads {args[0] if args else 'script'} into current shell",
        'touch': lambda args: f"creates/updates timestamp of {args[0] if args else 'file'}",
        'head': lambda args: f"shows first lines of {args[-1] if args else 'file'}",
        'tail': lambda args: f"shows last lines of {args[-1] if args else 'file'}",
        'sort': lambda args: "sorts input lines",
        'uniq': lambda args: "filters duplicate lines",
        'wc': lambda args: "counts lines/words/bytes",
        'awk': lambda args: "processes text with patterns",
        'sed': lambda args: "transforms text with patterns",
        'xargs': lambda args: "builds commands from input",
        'tee': lambda args: "splits output to file and stdout",
        'jq': lambda args: "processes JSON data",
        'less': lambda args: f"pages through {args[0] if args else 'input'}",
        'more': lambda args: f"pages through {args[0] if args else 'input'}",
        'node': lambda args: "executes Node.js script",
        'npx': lambda args: f"runs npm package {args[0] if args else 'command'}",
        'make': lambda args: f"runs make {args[0] if args else 'target'}",
        'cmake': lambda args: "configures CMake build",
        'cargo': lambda args: f"runs Cargo {args[0] if args else 'command'}",
        'rustc': lambda args: "compiles Rust code",
        'go': lambda args: f"runs Go {args[0] if args else 'command'}",
        'java': lambda args: "runs Java program",
        'javac': lambda args: "compiles Java source",
        'gcc': lambda args: "compiles C/C++ code",
        'clang': lambda args: "compiles code with Clang",
        'vim': lambda args: f"edits {args[0] if args else 'file'} in Vim",
        'nano': lambda args: f"edits {args[0] if args else 'file'} in nano",
        'emacs': lambda args: f"edits {args[0] if args else 'file'} in Emacs",
        'which': lambda args: f"locates {args[0] if args else 'command'} executable",
        'whereis': lambda args: f"finds {args[0] if args else 'command'} locations",
        'man': lambda args: f"shows manual for {args[0] if args else 'command'}",
        'pwd': lambda args: "prints current working directory",
        'whoami': lambda args: "prints current username",
        'date': lambda args: "displays current date/time",
        'env': lambda args: "displays environment variables",
        'set': lambda args: "sets shell options",
        'unset': lambda args: f"removes variable {args[0] if args else ''}",
        'read': lambda args: "reads input into variable",
        'test': lambda args: "evaluates conditional expression",
        '[': lambda args: "evaluates conditional expression",
        'if': lambda args: "conditional statement",
        'for': lambda args: "loop over items",
        'while': lambda args: "loop while condition true",
        'case': lambda args: "pattern matching statement",
        'start': lambda args: f"opens {args[0] if args else 'file/URL'} (Windows)",
        'open': lambda args: f"opens {args[0] if args else 'file/URL'} (macOS)",
        'xdg-open': lambda args: f"opens {args[0] if args else 'file/URL'} (Linux)",
        'code': lambda args: f"opens {args[0] if args else 'path'} in VS Code",
        'claude': lambda args: f"runs Claude CLI {args[0] if args else 'command'}",
    }

    # Get args (skip flags)
    args = [t for t in tokens[1:] if not t.startswith('-')]

    if base_cmd in descriptions:
        return descriptions[base_cmd](args)

    # Default description
    return f"executes {base_cmd} command"


def _describe_git_subcommand(args: list) -> str:
    """Describe git subcommands in detail."""
    if not args:
        return ""

    subcommand = args[0]
    git_descriptions = {
        'init': ' to initialize a new repository',
        'clone': ' to copy a remote repository',
        'add': ' to stage changes',
        'commit': ' to save staged changes',
        'push': ' to upload commits to remote',
        'pull': ' to download and merge remote changes',
        'fetch': ' to download remote changes',
        'merge': ' to combine branches',
        'rebase': ' to replay commits on new base',
        'checkout': ' to switch branches or restore files',
        'branch': ' to manage branches',
        'status': ' to show working tree status',
        'log': ' to show commit history',
        'diff': ' to show changes',
        'stash': ' to temporarily store changes',
        'reset': ' to undo changes',
        'remote': ' to manage remote connections',
        'tag': ' to manage tags',
    }

    return git_descriptions.get(subcommand, '')


def _parse_command(cmd_string: str) -> dict:
    """Parse a command string into components."""
    parts = cmd_string.strip().split()
    if not parts:
        return {"base": "", "flags": [], "args": []}

    base = parts[0]
    flags = []
    args = []

    for part in parts[1:]:
        if part.startswith("-"):
            flags.append(part)
        else:
            args.append(part)

    return {"base": base, "flags": flags, "args": args}


def _get_flag_description(cmd: str, flag: str) -> Optional[str]:
    """Get description for a flag of a command from merged sources."""
    merged = _get_flags_for_cmd(cmd)
    if flag in merged:
        return merged[flag]
    # Try individual characters for combined flags (e.g., -la -> -l, -a)
    if len(flag) > 2 and flag.startswith("-") and not flag.startswith("--"):
        for char in flag[1:]:
            single_flag = f"-{char}"
            if single_flag in merged:
                return merged[single_flag]
    return None


def _generate_distractor_flags(cmd: str, correct_flag: str, count: int = 3) -> list[str]:
    """Generate plausible distractor flags from merged knowledge sources."""
    distractors = []

    # Get other flags from the same command (merged sources)
    cmd_flags = _get_flags_for_cmd(cmd)
    if cmd_flags:
        other_flags = [f for f in cmd_flags.keys() if f != correct_flag]
        random.shuffle(other_flags)
        distractors.extend(other_flags[:count])

    # If we need more, get common flags from other commands
    if len(distractors) < count:
        for other_cmd in _get_all_flagged_commands():
            if other_cmd != cmd:
                for flag in _get_flags_for_cmd(other_cmd):
                    if flag not in distractors and flag != correct_flag:
                        distractors.append(flag)
                        if len(distractors) >= count:
                            break
            if len(distractors) >= count:
                break

    return distractors[:count]


def _generate_distractor_descriptions(correct_desc: str, count: int = 3) -> list[str]:
    """Generate plausible wrong descriptions using command-level descriptions for length parity."""
    distractors = []

    # First: collect command-level descriptions from COMMAND_DB (similar length to correct answer)
    cmd_descriptions = []
    for cmd_name in COMMAND_DB:
        cmd_info = COMMAND_DB[cmd_name]
        desc = cmd_info.get('description', '')
        if desc and desc.lower() != correct_desc.lower():
            # Truncate very long descriptions to similar length as correct answer
            max_len = max(len(correct_desc) + 40, 80)
            if len(desc) > max_len:
                desc = desc[:max_len].rsplit(' ', 1)[0] + '...'
            cmd_descriptions.append(desc)

    if cmd_descriptions:
        random.shuffle(cmd_descriptions)
        distractors.extend(cmd_descriptions[:count])

    # Fallback: use flag descriptions if not enough command descriptions
    if len(distractors) < count:
        all_flag_descs = []
        for cmd in _get_all_flagged_commands():
            all_flag_descs.extend(_get_flags_for_cmd(cmd).values())
        all_flag_descs = list(set(all_flag_descs))
        all_flag_descs = [d for d in all_flag_descs if d.lower() != correct_desc.lower()]
        random.shuffle(all_flag_descs)
        distractors.extend(all_flag_descs[:count - len(distractors)])

    # Remove duplicates
    seen = set()
    unique = []
    for d in distractors:
        dl = d.lower()
        if dl not in seen:
            seen.add(dl)
            unique.append(d)
    return unique[:count]


def generate_what_does_quiz(
    command: dict,
    analyzed_data: Optional[dict] = None
) -> QuizQuestion:
    """
    Generate a "What does this do?" quiz question.

    Args:
        command: Dictionary with keys like 'command', 'description', 'complexity', etc.
        analyzed_data: Optional additional analysis data

    Returns:
        QuizQuestion instance
    """
    cmd_string = command.get("command", "")
    complexity = command.get("complexity", 2)

    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    # Always use the educational bash description generator (not session descriptions)
    correct_desc = _generate_bash_description(cmd_string)
    # Capitalize first letter for consistent formatting
    if correct_desc:
        correct_desc = correct_desc[0].upper() + correct_desc[1:]

    # Add flag details if available
    flag_descs = []
    for flag in parsed["flags"]:
        fd = _get_flag_description(base_cmd, flag)
        if fd:
            flag_descs.append(f"{flag} ({fd.lower()})")
    if flag_descs:
        correct_desc += " using " + ", ".join(flag_descs)

    # Generate distractors
    distractor_descriptions = _generate_distractor_descriptions(correct_desc, 3)

    # Make distractors more plausible by relating to the command
    related_cmds = _get_related_commands(base_cmd)
    if related_cmds and len(distractor_descriptions) < 3:
        for rel_cmd in related_cmds[:3 - len(distractor_descriptions)]:
            distractor_descriptions.append(f"Runs {rel_cmd} to process files")

    # Ensure we have exactly 3 distractors with plausible alternatives
    fallback_actions = [
        f"List directory contents with detailed file information",
        f"Search recursively through files for matching patterns",
        f"Display or modify file permissions and ownership",
        f"Compress or archive files for storage and transfer",
        f"Monitor system processes and resource usage",
        f"Download files from a remote server or URL",
        f"Edit configuration files in the default text editor",
        f"Install or update packages from the package manager",
    ]
    random.shuffle(fallback_actions)
    fb_idx = 0
    while len(distractor_descriptions) < 3:
        if fb_idx < len(fallback_actions):
            fallback = fallback_actions[fb_idx]
            if fallback.lower() != correct_desc.lower():
                distractor_descriptions.append(fallback)
            fb_idx += 1
        else:
            distractor_descriptions.append(f"Run a system utility to process input data")

    # Create options (shuffle positions)
    options = []
    correct_id = "a"

    all_answers = [correct_desc] + distractor_descriptions[:3]
    random.shuffle(all_answers)

    for i, answer in enumerate(all_answers):
        opt_id = chr(ord('a') + i)
        is_correct = (answer == correct_desc)
        if is_correct:
            correct_id = opt_id
        options.append(QuizOption(
            id=opt_id,
            text=answer,
            is_correct=is_correct,
            explanation=f"{'Correct!' if is_correct else 'Incorrect.'} This command: {correct_desc}"
        ))

    question_id = _generate_id(f"what_does_{cmd_string}")

    return QuizQuestion(
        id=question_id,
        quiz_type=QuizType.WHAT_DOES,
        question_text=f"What does this command do?\n\n```bash\n{cmd_string}\n```",
        options=options,
        correct_option_id=correct_id,
        explanation=f"The command `{cmd_string}` {correct_desc.lower()}",
        difficulty=min(complexity, 5),
        command_context=cmd_string,
        tags=[base_cmd, "what_does"]
    )


def generate_which_flag_quiz(
    command: dict,
    analyzed_data: Optional[dict] = None
) -> Optional[QuizQuestion]:
    """
    Generate a "Which flag?" quiz question.

    Args:
        command: Dictionary with command info
        analyzed_data: Optional additional analysis data

    Returns:
        QuizQuestion instance or None if not enough flag data
    """
    cmd_string = command.get("command", "")
    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    cmd_flags = _get_flags_for_cmd(base_cmd)
    if not cmd_flags or not parsed["flags"]:
        return None

    # Pick a flag to quiz on
    available_flags = [f for f in parsed["flags"] if f in cmd_flags]
    if not available_flags:
        return None

    target_flag = random.choice(available_flags)
    flag_desc = cmd_flags[target_flag]

    # Generate distractor flags
    distractor_flags = _generate_distractor_flags(base_cmd, target_flag, 3)

    # Ensure we have exactly 3 distractors
    while len(distractor_flags) < 3:
        fake_flag = f"-{random.choice('abcdefghjkmnopqrstuwxyz')}"
        if fake_flag not in distractor_flags and fake_flag != target_flag:
            distractor_flags.append(fake_flag)

    # Create options
    all_flags = [target_flag] + distractor_flags[:3]
    random.shuffle(all_flags)

    options = []
    correct_id = "a"

    for i, flag in enumerate(all_flags):
        opt_id = chr(ord('a') + i)
        is_correct = (flag == target_flag)
        if is_correct:
            correct_id = opt_id

        # Get description for option explanation
        flag_explanation = cmd_flags.get(flag, "Unknown flag")

        options.append(QuizOption(
            id=opt_id,
            text=flag,
            is_correct=is_correct,
            explanation=f"{flag}: {flag_explanation}" if flag in cmd_flags else f"{flag}: Not a standard flag for {base_cmd}"
        ))

    question_id = _generate_id(f"which_flag_{base_cmd}_{target_flag}")

    return QuizQuestion(
        id=question_id,
        quiz_type=QuizType.WHICH_FLAG,
        question_text=f"You want to **{flag_desc.lower()}** when using `{base_cmd}`. Which flag should you use?",
        options=options,
        correct_option_id=correct_id,
        explanation=f"The `{target_flag}` flag in `{base_cmd}` is used to {flag_desc.lower()}",
        difficulty=2,
        command_context=base_cmd,
        tags=[base_cmd, "which_flag"]
    )


def generate_build_command_quiz(
    command: dict,
    analyzed_data: Optional[dict] = None
) -> QuizQuestion:
    """
    Generate a "Build the command" quiz question.

    Args:
        command: Dictionary with command info including intent/description
        analyzed_data: Optional additional analysis data

    Returns:
        QuizQuestion instance
    """
    cmd_string = command.get("command", "")

    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    # Use the original command string as correct answer (preserves flag-argument ordering)
    correct_answer = cmd_string.strip()

    # Generate wrong arrangements using parsed components
    all_parts = [base_cmd] + parsed["flags"] + parsed["args"]
    distractors = []

    # Distractor 1: Wrong order of components
    if len(all_parts) > 2:
        wrong_order = all_parts.copy()
        random.shuffle(wrong_order)
        wrong_str = " ".join(wrong_order)
        if wrong_str != correct_answer:
            distractors.append(wrong_str)

    # Distractor 2: Missing flag
    if parsed["flags"]:
        missing_flag = [base_cmd] + parsed["flags"][:-1] + parsed["args"]
        distractors.append(" ".join(missing_flag))

    # Distractor 3: Wrong flag
    if parsed["flags"] and _get_flags_for_cmd(base_cmd):
        wrong_flags = _generate_distractor_flags(base_cmd, parsed["flags"][0], 1)
        if wrong_flags:
            wrong_flag_cmd = [base_cmd] + [wrong_flags[0]] + parsed["flags"][1:] + parsed["args"]
            distractors.append(" ".join(wrong_flag_cmd))

    # Distractor 4: Related but wrong command
    related = _get_related_commands(base_cmd)
    if related:
        wrong_cmd = [related[0]] + parsed["flags"] + parsed["args"]
        distractors.append(" ".join(wrong_cmd))

    # Ensure we have exactly 3 distractors with plausible alternatives
    # Use real flags from the knowledge base as fallback distractors
    all_cmd_flags = list(_get_flags_for_cmd(base_cmd).keys())
    random.shuffle(all_cmd_flags)
    fb_flag_idx = 0
    while len(distractors) < 3:
        if fb_flag_idx < len(all_cmd_flags):
            fallback_flag = all_cmd_flags[fb_flag_idx]
            fallback_cmd = f"{base_cmd} {fallback_flag} {' '.join(parsed['args'])}"
            if fallback_cmd.strip() != correct_answer:
                distractors.append(fallback_cmd.strip())
            fb_flag_idx += 1
        else:
            # Use a related command as last resort
            related = _get_related_commands(base_cmd)
            if related:
                rel = related[len(distractors) % len(related)]
                distractors.append(f"{rel} {' '.join(parsed['flags'])} {' '.join(parsed['args'])}".strip())
            else:
                distractors.append(f"{base_cmd} {' '.join(parsed['args'])}".strip())

    # Remove duplicates and correct answer from distractors
    distractors = list(set(d for d in distractors if d != correct_answer))[:3]
    while len(distractors) < 3:
        distractors.append(f"{base_cmd} {' '.join(parsed['args'])}".strip())

    # Create options
    all_answers = [correct_answer] + distractors[:3]
    random.shuffle(all_answers)

    options = []
    correct_id = "a"

    for i, answer in enumerate(all_answers):
        opt_id = chr(ord('a') + i)
        is_correct = (answer == correct_answer)
        if is_correct:
            correct_id = opt_id
        options.append(QuizOption(
            id=opt_id,
            text=f"`{answer}`",
            is_correct=is_correct,
            explanation="Correct command structure" if is_correct else "Incorrect command structure"
        ))

    question_id = _generate_id(f"build_{cmd_string}")

    # Always generate description from the command itself (not session descriptions)
    task_description = _generate_bash_description(cmd_string)

    return QuizQuestion(
        id=question_id,
        quiz_type=QuizType.BUILD_COMMAND,
        question_text=f"Build the correct command to **{task_description}**.\n\nWhich command is correct?",
        options=options,
        correct_option_id=correct_id,
        explanation=f"The correct command is `{correct_answer}` - this properly accomplishes the task",
        difficulty=3,
        command_context=cmd_string,
        tags=[base_cmd, "build_command"]
    )


def generate_spot_difference_quiz(
    cmd1: dict,
    cmd2: dict
) -> Optional[QuizQuestion]:
    """
    Generate a "Spot the difference" quiz question.

    Args:
        cmd1: First command dictionary
        cmd2: Second command dictionary (should be similar but different)

    Returns:
        QuizQuestion instance or None if commands aren't suitable
    """
    cmd1_string = cmd1.get("command", "")
    cmd2_string = cmd2.get("command", "")

    parsed1 = _parse_command(cmd1_string)
    parsed2 = _parse_command(cmd2_string)

    # Commands should have same base
    if parsed1["base"] != parsed2["base"]:
        return None

    base_cmd = parsed1["base"]

    # Find the differences
    flags1 = set(parsed1["flags"])
    flags2 = set(parsed2["flags"])

    only_in_1 = flags1 - flags2
    only_in_2 = flags2 - flags1

    if not only_in_1 and not only_in_2:
        # Check if args are different
        if parsed1["args"] == parsed2["args"]:
            return None

    # Build the correct explanation of difference
    differences = []
    has_unknown = False
    for flag_set, label in [(only_in_1, "Command 1"), (only_in_2, "Command 2")]:
        for flag in flag_set:
            desc = _get_flag_description(base_cmd, flag)
            # Handle numeric flags like -3 (shorthand for -n 3)
            if not desc and re.match(r'^-\d+$', flag):
                desc = f"Specify count ({flag[1:]})"
            if not desc:
                has_unknown = True
            differences.append(f"{label} has `{flag}` ({desc or 'specifies an option'})")
    # Skip questions where we can't explain the flags well
    if has_unknown:
        return None
    if parsed1["args"] != parsed2["args"]:
        differences.append(f"Different arguments: '{' '.join(parsed1['args'])}' vs '{' '.join(parsed2['args'])}'")

    correct_explanation = "; ".join(differences) if differences else "Different arguments or options"

    # Generate distractor explanations
    distractors = [
        "Both commands do exactly the same thing",
        f"Command 1 runs faster than Command 2",
        f"Command 2 is deprecated, Command 1 is the modern version",
        f"Command 1 modifies files, Command 2 only reads them",
        f"Command 2 requires root permissions, Command 1 doesn't"
    ]
    random.shuffle(distractors)
    distractor_explanations = distractors[:3]

    # Create options
    all_answers = [correct_explanation] + distractor_explanations
    random.shuffle(all_answers)

    options = []
    correct_id = "a"

    for i, answer in enumerate(all_answers):
        opt_id = chr(ord('a') + i)
        is_correct = (answer == correct_explanation)
        if is_correct:
            correct_id = opt_id
        options.append(QuizOption(
            id=opt_id,
            text=answer,
            is_correct=is_correct,
            explanation="Correct analysis" if is_correct else "Incorrect analysis"
        ))

    question_id = _generate_id(f"spot_diff_{cmd1_string}_{cmd2_string}")

    return QuizQuestion(
        id=question_id,
        quiz_type=QuizType.SPOT_DIFFERENCE,
        question_text=f"What is the key difference between these two commands?\n\n**Command 1:**\n```bash\n{cmd1_string}\n```\n\n**Command 2:**\n```bash\n{cmd2_string}\n```",
        options=options,
        correct_option_id=correct_id,
        explanation=f"The key difference is: {correct_explanation}",
        difficulty=4,
        command_context=f"{cmd1_string} vs {cmd2_string}",
        tags=[base_cmd, "spot_difference"]
    )


def _create_similar_command_variant(command: dict) -> Optional[dict]:
    """Create a similar but different command for spot-the-difference."""
    cmd_string = command.get("command", "")
    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    variant_flags = _get_flags_for_cmd(base_cmd)
    if not variant_flags:
        return None

    # Strategy: add, remove, or change a flag
    strategies = []

    # Can add a flag
    available_flags = [f for f in variant_flags.keys() if f not in parsed["flags"]]
    if available_flags:
        strategies.append("add")

    # Can remove a flag
    if parsed["flags"]:
        strategies.append("remove")

    # Can change a flag
    if parsed["flags"] and available_flags:
        strategies.append("change")

    if not strategies:
        return None

    strategy = random.choice(strategies)
    new_flags = parsed["flags"].copy()

    if strategy == "add" and available_flags:
        new_flags.append(random.choice(available_flags))
    elif strategy == "remove" and new_flags:
        new_flags.pop(random.randint(0, len(new_flags) - 1))
    elif strategy == "change" and new_flags and available_flags:
        idx = random.randint(0, len(new_flags) - 1)
        new_flags[idx] = random.choice(available_flags)

    new_cmd = " ".join([base_cmd] + new_flags + parsed["args"])

    return {
        "command": new_cmd,
        "description": f"Variant of {cmd_string}",
        "complexity": command.get("complexity", 2)
    }


def generate_quiz_set(
    analyzed_commands: list[dict],
    count: int = 20
) -> list[QuizQuestion]:
    """
    Generate a set of quiz questions from analyzed commands.

    Args:
        analyzed_commands: List of analyzed command dictionaries
        count: Target number of questions (default 20)

    Returns:
        List of QuizQuestion instances
    """
    questions: list[QuizQuestion] = []

    # Filter out non-bash entries (Python code fragments, junk tokens, single chars)
    junk_tokens = {'version', 'total', 'package', 'success', 'error', 'reading',
                   'editing', 'done', 'warning', 'info', 'note', 'output',
                   'task', 'goal', 'purpose', 'what', 'description'}
    clean_commands = []
    for cmd in analyzed_commands:
        base = cmd.get("base_command", "")
        if not base or len(base) < 2:
            continue
        if any(c in base for c in ('(', ')', '=', '{', '}')):
            continue
        if any(c in base for c in ('\\', '"', "'")) or '&' in base:
            continue
        if base[0].isupper() and base.isalpha() and base not in ('PATH', 'HOME'):
            continue
        if base.lower() in junk_tokens:
            continue
        clean_commands.append(cmd)

    # Filter commands by complexity >= 2
    eligible_commands = [
        cmd for cmd in clean_commands
        if cmd.get("complexity", 0) >= 2
    ]

    if not eligible_commands:
        eligible_commands = clean_commands if clean_commands else analyzed_commands

    # Weight toward high-frequency commands
    weighted_commands = []
    for cmd in eligible_commands:
        frequency = cmd.get("frequency", 1)
        weight = min(frequency, 5)  # Cap weight at 5
        weighted_commands.extend([cmd] * weight)

    if not weighted_commands:
        weighted_commands = eligible_commands

    # Calculate target counts for each quiz type
    # Distribution: 40% what_does, 25% which_flag, 20% build, 15% spot_diff
    target_what_does = max(1, int(count * 0.4))
    target_which_flag = max(1, int(count * 0.25))
    target_build = max(1, int(count * 0.2))
    target_spot_diff = max(1, int(count * 0.15))

    # Track used commands per quiz type to avoid repeating the same command
    used_per_type = {
        QuizType.WHAT_DOES: set(),
        QuizType.WHICH_FLAG: set(),
        QuizType.BUILD_COMMAND: set(),
        QuizType.SPOT_DIFFERENCE: set(),
    }

    # Max command length for readable quiz questions
    MAX_QUIZ_CMD_LEN = 200

    # Generate "What does this do?" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.WHAT_DOES]) >= target_what_does:
            break
        cmd_id = cmd.get("command", "")
        if len(cmd_id) > MAX_QUIZ_CMD_LEN:
            continue
        if cmd_id not in used_per_type[QuizType.WHAT_DOES]:
            q = generate_what_does_quiz(cmd)
            questions.append(q)
            used_per_type[QuizType.WHAT_DOES].add(cmd_id)

    # Generate "Which flag?" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.WHICH_FLAG]) >= target_which_flag:
            break
        cmd_id = cmd.get("command", "")
        if cmd_id not in used_per_type[QuizType.WHICH_FLAG]:
            q = generate_which_flag_quiz(cmd)
            if q:
                questions.append(q)
                used_per_type[QuizType.WHICH_FLAG].add(cmd_id)

    # Generate "Build the command" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.BUILD_COMMAND]) >= target_build:
            break
        cmd_id = cmd.get("command", "")
        if len(cmd_id) > MAX_QUIZ_CMD_LEN:
            continue
        if cmd_id not in used_per_type[QuizType.BUILD_COMMAND]:
            q = generate_build_command_quiz(cmd)
            questions.append(q)
            used_per_type[QuizType.BUILD_COMMAND].add(cmd_id)

    # Generate "Spot the difference" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.SPOT_DIFFERENCE]) >= target_spot_diff:
            break
        cmd_id = cmd.get("command", "")
        if len(cmd_id) > MAX_QUIZ_CMD_LEN:
            continue
        if cmd_id not in used_per_type[QuizType.SPOT_DIFFERENCE]:
            variant = _create_similar_command_variant(cmd)
            if variant:
                q = generate_spot_difference_quiz(cmd, variant)
                if q:
                    questions.append(q)
                    used_per_type[QuizType.SPOT_DIFFERENCE].add(cmd_id)

    # Deduplicate by question text (same question can come from different commands)
    seen_texts = set()
    deduped = []
    for q in questions:
        # Normalize: take first 80 chars of question text
        q_key = q.question_text[:80]
        if q_key not in seen_texts:
            deduped.append(q)
            seen_texts.add(q_key)
    questions = deduped

    # Shuffle final questions
    random.shuffle(questions)

    # Trim to target count
    return questions[:count]


def create_quiz(
    analyzed_commands: list[dict],
    title: str = "Bash Command Quiz",
    description: str = "Test your bash command knowledge",
    question_count: int = 20,
    time_limit: Optional[int] = None
) -> Quiz:
    """
    Create a complete quiz from analyzed commands.

    Args:
        analyzed_commands: List of analyzed command dictionaries
        title: Quiz title
        description: Quiz description
        question_count: Target number of questions
        time_limit: Optional time limit in seconds

    Returns:
        Quiz instance
    """
    questions = generate_quiz_set(analyzed_commands, question_count)

    quiz_id = _generate_id(f"{title}_{len(questions)}")

    return Quiz(
        id=quiz_id,
        title=title,
        description=description,
        questions=questions,
        time_limit_seconds=time_limit
    )


def generate_quizzes(
    commands: list[dict],
    analysis: dict,
    question_count: int = 20
) -> list[dict]:
    """
    Generate quizzes from commands and analysis for the pipeline.

    This is the interface expected by main.py.

    Args:
        commands: List of command dictionaries
        analysis: Analysis dictionary from analyze_commands
        question_count: Target number of questions

    Returns:
        List of quiz question dictionaries
    """
    # Get analyzed commands from analysis if available, otherwise use raw commands
    analyzed_commands = analysis.get('commands', commands)

    if not analyzed_commands:
        return []

    # Generate quiz questions
    questions = generate_quiz_set(analyzed_commands, question_count)

    # Convert QuizQuestion objects to dictionaries using the built-in method
    return [q.to_dict() for q in questions]


# =============================================================================
# Main entry point for testing
# =============================================================================

if __name__ == "__main__":
    import json

    # Example analyzed commands for testing
    sample_commands = [
        {
            "command": "ls -la /var/log",
            "description": "List all files including hidden ones in /var/log with detailed info",
            "complexity": 3,
            "frequency": 5
        },
        {
            "command": "grep -rn 'error' /var/log",
            "description": "Search recursively for 'error' with line numbers in /var/log",
            "complexity": 3,
            "frequency": 4
        },
        {
            "command": "find . -name '*.py' -type f",
            "description": "Find all Python files in current directory",
            "complexity": 4,
            "frequency": 3
        },
        {
            "command": "tar -czvf backup.tar.gz /home/user",
            "description": "Create a gzipped tar archive of /home/user",
            "complexity": 4,
            "frequency": 2
        },
        {
            "command": "chmod -R 755 /var/www",
            "description": "Recursively set permissions to 755 on /var/www",
            "complexity": 3,
            "frequency": 2
        },
        {
            "command": "curl -sL https://example.com/api",
            "description": "Silently fetch URL following redirects",
            "complexity": 3,
            "frequency": 4
        },
        {
            "command": "ps aux | grep python",
            "description": "List all processes and filter for python",
            "complexity": 3,
            "frequency": 5
        },
        {
            "command": "sed -i 's/old/new/g' file.txt",
            "description": "Replace all occurrences of 'old' with 'new' in-place",
            "complexity": 4,
            "frequency": 2
        },
        {
            "command": "sort -u names.txt",
            "description": "Sort file and remove duplicate lines",
            "complexity": 2,
            "frequency": 3
        },
        {
            "command": "du -sh /home/*",
            "description": "Show disk usage summary for each home directory",
            "complexity": 2,
            "frequency": 4
        }
    ]

    # Generate quiz
    quiz = create_quiz(
        sample_commands,
        title="Bash Fundamentals Quiz",
        description="Test your knowledge of common bash commands",
        question_count=15
    )

    # Print quiz as JSON
    print(json.dumps(quiz.to_dict(), indent=2))

    print(f"\n=== Generated {len(quiz.questions)} questions ===")
    for i, q in enumerate(quiz.questions, 1):
        print(f"\n{i}. [{q.quiz_type.value}] {q.question_text[:80]}...")
