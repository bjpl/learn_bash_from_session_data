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
    """Get description for a flag of a command."""
    if cmd in FLAG_DATABASE:
        # Handle flags like -la (combined short flags)
        if flag in FLAG_DATABASE[cmd]:
            return FLAG_DATABASE[cmd][flag]
        # Try individual characters for combined flags
        if len(flag) > 2 and flag.startswith("-") and not flag.startswith("--"):
            for char in flag[1:]:
                single_flag = f"-{char}"
                if single_flag in FLAG_DATABASE[cmd]:
                    return FLAG_DATABASE[cmd][single_flag]
    return None


def _generate_distractor_flags(cmd: str, correct_flag: str, count: int = 3) -> list[str]:
    """Generate plausible distractor flags."""
    distractors = []

    # Get other flags from the same command
    if cmd in FLAG_DATABASE:
        other_flags = [f for f in FLAG_DATABASE[cmd].keys() if f != correct_flag]
        random.shuffle(other_flags)
        distractors.extend(other_flags[:count])

    # If we need more, get common flags from other commands
    if len(distractors) < count:
        for other_cmd, flags in FLAG_DATABASE.items():
            if other_cmd != cmd:
                for flag in flags:
                    if flag not in distractors and flag != correct_flag:
                        distractors.append(flag)
                        if len(distractors) >= count:
                            break
            if len(distractors) >= count:
                break

    return distractors[:count]


def _generate_distractor_descriptions(correct_desc: str, count: int = 3) -> list[str]:
    """Generate plausible wrong descriptions."""
    distractors = []

    # Collect all descriptions from FLAG_DATABASE
    all_descriptions = []
    for cmd_flags in FLAG_DATABASE.values():
        all_descriptions.extend(cmd_flags.values())

    # Remove duplicates and the correct answer
    all_descriptions = list(set(all_descriptions))
    all_descriptions = [d for d in all_descriptions if d.lower() != correct_desc.lower()]

    random.shuffle(all_descriptions)
    return all_descriptions[:count]


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
    description = command.get("description", "")
    complexity = command.get("complexity", 2)

    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    # Build the correct description
    correct_desc = description
    if not correct_desc:
        # Generate from flags
        flag_descs = []
        for flag in parsed["flags"]:
            fd = _get_flag_description(base_cmd, flag)
            if fd:
                flag_descs.append(fd)
        correct_desc = f"Runs {base_cmd}"
        if flag_descs:
            correct_desc += " with: " + ", ".join(flag_descs)

    # Generate distractors
    distractor_descriptions = _generate_distractor_descriptions(correct_desc, 3)

    # Make distractors more plausible by relating to the command
    related_cmds = _get_related_commands(base_cmd)
    if related_cmds and len(distractor_descriptions) < 3:
        for rel_cmd in related_cmds[:3 - len(distractor_descriptions)]:
            distractor_descriptions.append(f"Runs {rel_cmd} to process files")

    # Ensure we have exactly 3 distractors
    while len(distractor_descriptions) < 3:
        distractor_descriptions.append(f"Performs an unrelated {base_cmd} operation")

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

    if base_cmd not in FLAG_DATABASE or not parsed["flags"]:
        return None

    # Pick a flag to quiz on
    available_flags = [f for f in parsed["flags"] if f in FLAG_DATABASE.get(base_cmd, {})]
    if not available_flags:
        return None

    target_flag = random.choice(available_flags)
    flag_desc = FLAG_DATABASE[base_cmd][target_flag]

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
        flag_explanation = FLAG_DATABASE.get(base_cmd, {}).get(flag, "Unknown flag")

        options.append(QuizOption(
            id=opt_id,
            text=flag,
            is_correct=is_correct,
            explanation=f"{flag}: {flag_explanation}" if flag in FLAG_DATABASE.get(base_cmd, {}) else f"{flag}: Not a standard flag for {base_cmd}"
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
    description = command.get("description", "")
    intent = command.get("intent", description)

    parsed = _parse_command(cmd_string)
    base_cmd = parsed["base"]

    # Create the correct command structure
    correct_components = [base_cmd] + parsed["flags"] + parsed["args"]
    correct_answer = " ".join(correct_components)

    # Generate wrong arrangements
    distractors = []

    # Distractor 1: Wrong order
    if len(correct_components) > 2:
        wrong_order = correct_components.copy()
        random.shuffle(wrong_order)
        if wrong_order != correct_components:
            distractors.append(" ".join(wrong_order))

    # Distractor 2: Missing flag
    if parsed["flags"]:
        missing_flag = [base_cmd] + parsed["flags"][:-1] + parsed["args"]
        distractors.append(" ".join(missing_flag))

    # Distractor 3: Wrong flag
    if parsed["flags"] and base_cmd in FLAG_DATABASE:
        wrong_flags = _generate_distractor_flags(base_cmd, parsed["flags"][0], 1)
        if wrong_flags:
            wrong_flag_cmd = [base_cmd] + [wrong_flags[0]] + parsed["flags"][1:] + parsed["args"]
            distractors.append(" ".join(wrong_flag_cmd))

    # Distractor 4: Related but wrong command
    related = _get_related_commands(base_cmd)
    if related:
        wrong_cmd = [related[0]] + parsed["flags"] + parsed["args"]
        distractors.append(" ".join(wrong_cmd))

    # Ensure we have exactly 3 distractors
    while len(distractors) < 3:
        # Add a clearly wrong option
        distractors.append(f"{base_cmd} --invalid-option")

    # Remove duplicates and correct answer from distractors
    distractors = list(set(d for d in distractors if d != correct_answer))[:3]
    while len(distractors) < 3:
        distractors.append(f"{base_cmd} --wrong-flag")

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

    task_description = intent if intent else f"perform the operation: {description}"

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
    if only_in_1:
        for flag in only_in_1:
            desc = _get_flag_description(base_cmd, flag)
            differences.append(f"Command 1 has `{flag}` ({desc or 'unknown'})")
    if only_in_2:
        for flag in only_in_2:
            desc = _get_flag_description(base_cmd, flag)
            differences.append(f"Command 2 has `{flag}` ({desc or 'unknown'})")
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

    if base_cmd not in FLAG_DATABASE:
        return None

    # Strategy: add, remove, or change a flag
    strategies = []

    # Can add a flag
    available_flags = [f for f in FLAG_DATABASE[base_cmd].keys() if f not in parsed["flags"]]
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

    # Filter commands by complexity >= 2
    eligible_commands = [
        cmd for cmd in analyzed_commands
        if cmd.get("complexity", 0) >= 2
    ]

    if not eligible_commands:
        eligible_commands = analyzed_commands

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

    used_commands = set()

    # Generate "What does this do?" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.WHAT_DOES]) >= target_what_does:
            break
        cmd_id = cmd.get("command", "")
        if cmd_id not in used_commands:
            q = generate_what_does_quiz(cmd)
            questions.append(q)
            used_commands.add(cmd_id)

    # Generate "Which flag?" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.WHICH_FLAG]) >= target_which_flag:
            break
        q = generate_which_flag_quiz(cmd)
        if q:
            questions.append(q)

    # Generate "Build the command" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.BUILD_COMMAND]) >= target_build:
            break
        q = generate_build_command_quiz(cmd)
        questions.append(q)

    # Generate "Spot the difference" questions
    random.shuffle(weighted_commands)
    for cmd in weighted_commands:
        if len([q for q in questions if q.quiz_type == QuizType.SPOT_DIFFERENCE]) >= target_spot_diff:
            break
        variant = _create_similar_command_variant(cmd)
        if variant:
            q = generate_spot_difference_quiz(cmd, variant)
            if q:
                questions.append(q)

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
