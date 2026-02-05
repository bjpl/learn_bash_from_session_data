"""
Analysis engine for bash command extraction and learning.

This module provides complexity scoring, category assignment, deduplication,
and statistics generation for extracted bash commands.
"""

import re
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Any, Optional

from knowledge_base import (
    COMMAND_TO_CATEGORY,
    PIPE_OPERATORS,
    REDIRECT_OPERATORS,
    COMPOUND_OPERATORS,
    SUBSHELL_MARKERS,
    PROCESS_SUBSTITUTION,
    LOOP_KEYWORDS,
    CONDITIONAL_KEYWORDS,
    LEARNING_ORDER,
    get_category,
    get_all_categories,
)


@dataclass
class ParsedCommand:
    """Represents a parsed bash command with its components."""
    raw: str
    base_command: str
    args: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
    has_pipe: bool = False
    has_redirect: bool = False
    has_compound: bool = False
    has_subshell: bool = False
    has_process_sub: bool = False
    has_loop: bool = False
    has_conditional: bool = False
    pipe_count: int = 0
    command_count: int = 1


@dataclass
class AnalysisResult:
    """Results from analyzing a set of commands."""
    total_commands: int
    unique_commands: int
    unique_base_commands: int
    complexity_distribution: Dict[int, int]
    category_breakdown: Dict[str, int]
    top_commands: List[Tuple[str, int]]
    top_base_commands: List[Tuple[str, int]]
    deduplicated_commands: List[Dict[str, Any]]
    fuzzy_groups: Dict[str, List[str]]
    statistics: Dict[str, Any]


def parse_command(raw_cmd: str) -> ParsedCommand:
    """
    Parse a raw command string into its components.

    Args:
        raw_cmd: The raw command string to parse

    Returns:
        ParsedCommand with extracted components
    """
    raw_cmd = raw_cmd.strip()

    # Initialize result
    result = ParsedCommand(raw=raw_cmd, base_command="")

    if not raw_cmd:
        return result

    # Check for various operators and constructs
    result.has_pipe = any(op in raw_cmd for op in PIPE_OPERATORS)
    result.has_redirect = any(op in raw_cmd for op in REDIRECT_OPERATORS)
    result.has_compound = any(op in raw_cmd for op in COMPOUND_OPERATORS)
    result.has_subshell = any(marker in raw_cmd for marker in SUBSHELL_MARKERS)
    result.has_process_sub = any(marker in raw_cmd for marker in PROCESS_SUBSTITUTION)

    # Check for loops and conditionals
    words = set(re.findall(r'\b\w+\b', raw_cmd))
    result.has_loop = bool(words & LOOP_KEYWORDS)
    result.has_conditional = bool(words & CONDITIONAL_KEYWORDS)

    # Count pipes
    result.pipe_count = raw_cmd.count('|') - raw_cmd.count('||')

    # Count commands (separated by pipes, && or ||, or ;)
    result.command_count = 1 + result.pipe_count + raw_cmd.count('&&') + raw_cmd.count('||') + raw_cmd.count(';')

    # Extract base command (first word, handling various prefixes)
    # Skip common prefixes like sudo, env, time, nice, etc.
    prefix_commands = {'sudo', 'env', 'time', 'nice', 'nohup', 'strace', 'ltrace', 'timeout'}

    # Get first segment (before any pipe or compound operator)
    first_segment = re.split(r'[|;&]', raw_cmd)[0].strip()

    # Tokenize the first segment
    tokens = first_segment.split()

    # Skip prefix commands to find the actual base command
    base_idx = 0
    while base_idx < len(tokens) and tokens[base_idx] in prefix_commands:
        base_idx += 1

    if base_idx < len(tokens):
        base_cmd = tokens[base_idx]
        # Handle env VAR=value cmd pattern
        while base_idx < len(tokens) and '=' in tokens[base_idx]:
            base_idx += 1
        if base_idx < len(tokens):
            base_cmd = tokens[base_idx]
        result.base_command = base_cmd

        # Extract flags and args from remaining tokens
        for token in tokens[base_idx + 1:]:
            if token.startswith('-'):
                result.flags.append(token)
            elif '=' not in token:
                result.args.append(token)

    return result


def score_complexity(parsed_cmd: ParsedCommand) -> int:
    """
    Score the complexity of a parsed command from 1-5.

    Complexity levels:
        1: Single command, no flags (ls, pwd, cd src)
        2: Single command with flags (ls -la, grep -r "pattern" .)
        3: Pipes or redirects (cat file | grep pattern)
        4: Compound commands, subshells, loops (find . -name "*.ts" | xargs grep)
        5: Complex pipelines, process substitution, multi-line

    Args:
        parsed_cmd: The parsed command to score

    Returns:
        Complexity score from 1 to 5
    """
    if not parsed_cmd.raw:
        return 1

    score = 1

    # Level 2: Has flags or multiple arguments
    if parsed_cmd.flags or len(parsed_cmd.args) > 1:
        score = max(score, 2)

    # Level 3: Has pipes or redirects
    if parsed_cmd.has_pipe or parsed_cmd.has_redirect:
        score = max(score, 3)

    # Level 4: Compound commands, subshells, loops, or multiple pipes
    if (parsed_cmd.has_compound or parsed_cmd.has_subshell or
        parsed_cmd.has_loop or parsed_cmd.pipe_count >= 2):
        score = max(score, 4)

    # Level 5: Process substitution, conditionals with pipes, or very complex
    if (parsed_cmd.has_process_sub or
        (parsed_cmd.has_conditional and parsed_cmd.has_pipe) or
        parsed_cmd.command_count >= 4 or
        parsed_cmd.pipe_count >= 3):
        score = max(score, 5)

    # Additional complexity factors
    raw = parsed_cmd.raw

    # Check for inline scripts or complex patterns
    complex_patterns = [
        r'\$\{[^}]+\}',           # Parameter expansion
        r'\$\([^)]+\)',           # Command substitution
        r'`[^`]+`',               # Backtick command substitution
        r'\[\[.*\]\]',            # Extended test
        r'<<<',                    # Here string
        r'<<\s*\w+',              # Here document
        r'\(\s*\)',               # Empty subshell or function
        r'{\s*\w+.*;',            # Brace expansion with commands
    ]

    complex_count = sum(1 for p in complex_patterns if re.search(p, raw))
    if complex_count >= 2:
        score = min(5, score + 1)

    return score


def assign_category(parsed_cmd: ParsedCommand) -> str:
    """
    Assign a category to a parsed command based on its base command.

    Args:
        parsed_cmd: The parsed command to categorize

    Returns:
        Category name string
    """
    if not parsed_cmd.base_command:
        return "Unknown"

    # Look up in knowledge base
    category = get_category(parsed_cmd.base_command)

    # If not found, try to infer from common patterns
    if category == "Unknown":
        base = parsed_cmd.base_command.lower()

        # Git subcommands (git-xxx or things that look git-related)
        if base.startswith('git-') or 'commit' in base or 'branch' in base:
            return "Git"

        # Development tools patterns
        if any(ext in base for ext in ['make', 'build', 'compile', 'test']):
            return "Development"

        # Network-related patterns
        if any(net in base for net in ['http', 'ftp', 'ssh', 'net', 'port']):
            return "Networking"

        # Package management patterns
        if any(pkg in base for pkg in ['install', 'update', 'upgrade', 'remove']):
            return "Package Management"

    return category


def _normalize_for_fuzzy(cmd: str) -> str:
    """
    Normalize a command for fuzzy deduplication.

    Replaces specific arguments with placeholders while keeping structure.
    """
    normalized = cmd

    # Replace quoted strings with placeholder
    normalized = re.sub(r'"[^"]*"', '"<STR>"', normalized)
    normalized = re.sub(r"'[^']*'", "'<STR>'", normalized)

    # Replace file paths with placeholder
    normalized = re.sub(r'(?<=[=\s])/[^\s]+', '<PATH>', normalized)
    normalized = re.sub(r'(?<=[=\s])\./[^\s]+', '<PATH>', normalized)
    normalized = re.sub(r'(?<=[=\s])~/[^\s]+', '<PATH>', normalized)

    # Replace numbers with placeholder
    normalized = re.sub(r'\b\d+\b', '<NUM>', normalized)

    # Replace UUIDs/hashes with placeholder
    normalized = re.sub(r'\b[a-f0-9]{32,}\b', '<HASH>', normalized)
    normalized = re.sub(r'\b[a-f0-9-]{36}\b', '<UUID>', normalized)

    # Replace IP addresses with placeholder
    normalized = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', normalized)

    # Replace URLs with placeholder
    normalized = re.sub(r'https?://[^\s]+', '<URL>', normalized)

    return normalized


def _get_command_signature(parsed_cmd: ParsedCommand) -> str:
    """
    Get a structural signature for a command (for fuzzy grouping).
    """
    parts = [parsed_cmd.base_command]

    # Add sorted flags (structure matters, not order)
    if parsed_cmd.flags:
        parts.append('FLAGS:' + ','.join(sorted(parsed_cmd.flags)))

    # Add argument count
    parts.append(f'ARGS:{len(parsed_cmd.args)}')

    # Add structural markers
    if parsed_cmd.has_pipe:
        parts.append(f'PIPES:{parsed_cmd.pipe_count}')
    if parsed_cmd.has_redirect:
        parts.append('REDIR')
    if parsed_cmd.has_compound:
        parts.append('COMPOUND')
    if parsed_cmd.has_subshell:
        parts.append('SUBSHELL')

    return '|'.join(parts)


def deduplicate(commands: List[str]) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
    """
    Deduplicate commands using both exact and fuzzy matching.

    Args:
        commands: List of raw command strings

    Returns:
        Tuple of (deduplicated command list with metadata, fuzzy groups)
    """
    # Exact deduplication with frequency counting
    exact_counts = Counter(commands)

    # Parse each unique command
    unique_parsed: Dict[str, ParsedCommand] = {}
    for cmd in exact_counts.keys():
        unique_parsed[cmd] = parse_command(cmd)

    # Group by fuzzy signature
    fuzzy_groups: Dict[str, List[str]] = defaultdict(list)
    for cmd, parsed in unique_parsed.items():
        signature = _get_command_signature(parsed)
        fuzzy_groups[signature].append(cmd)

    # Build deduplicated result
    deduplicated = []
    seen_signatures: Set[str] = set()

    for cmd in sorted(exact_counts.keys(), key=lambda x: -exact_counts[x]):
        parsed = unique_parsed[cmd]
        signature = _get_command_signature(parsed)

        is_fuzzy_duplicate = signature in seen_signatures
        seen_signatures.add(signature)

        deduplicated.append({
            'command': cmd,
            'frequency': exact_counts[cmd],
            'base_command': parsed.base_command,
            'complexity': score_complexity(parsed),
            'category': assign_category(parsed),
            'is_fuzzy_duplicate': is_fuzzy_duplicate,
            'fuzzy_signature': signature,
            'parsed': parsed,
        })

    # Convert fuzzy groups to regular dict with only groups > 1
    fuzzy_groups_filtered = {
        sig: cmds for sig, cmds in fuzzy_groups.items() if len(cmds) > 1
    }

    return deduplicated, fuzzy_groups_filtered


def generate_statistics(commands: List[str]) -> Dict[str, Any]:
    """
    Generate comprehensive statistics for a list of commands.

    Args:
        commands: List of raw command strings

    Returns:
        Dictionary containing various statistics
    """
    if not commands:
        return {
            'total_commands': 0,
            'unique_commands': 0,
            'unique_base_commands': 0,
            'complexity_distribution': {},
            'category_breakdown': {},
            'average_complexity': 0.0,
            'most_complex_commands': [],
        }

    # Parse all commands
    parsed_commands = [parse_command(cmd) for cmd in commands]

    # Basic counts
    total = len(commands)
    unique_cmds = set(commands)
    unique_count = len(unique_cmds)

    # Base command analysis
    base_commands = [p.base_command for p in parsed_commands if p.base_command]
    unique_base = set(base_commands)
    base_counts = Counter(base_commands)

    # Complexity analysis
    complexities = [score_complexity(p) for p in parsed_commands]
    complexity_dist = Counter(complexities)
    avg_complexity = sum(complexities) / len(complexities) if complexities else 0.0

    # Category analysis
    categories = [assign_category(p) for p in parsed_commands]
    category_counts = Counter(categories)

    # Find most complex commands
    cmd_complexity = [(p.raw, score_complexity(p)) for p in parsed_commands]
    most_complex = sorted(cmd_complexity, key=lambda x: -x[1])[:10]

    # Command frequency
    cmd_counts = Counter(commands)
    top_commands = cmd_counts.most_common(20)
    top_base = base_counts.most_common(20)

    return {
        'total_commands': total,
        'unique_commands': unique_count,
        'unique_base_commands': len(unique_base),
        'complexity_distribution': dict(sorted(complexity_dist.items())),
        'category_breakdown': dict(sorted(category_counts.items(), key=lambda x: -x[1])),
        'average_complexity': round(avg_complexity, 2),
        'most_complex_commands': most_complex,
        'top_commands': top_commands,
        'top_base_commands': top_base,
        'base_command_coverage': {
            cat: sum(1 for b in unique_base if get_category(b) == cat)
            for cat in get_all_categories()
        },
    }


def analyze_session(extracted_commands: List[str]) -> AnalysisResult:
    """
    Perform complete analysis of extracted commands from a session.

    Args:
        extracted_commands: List of command strings extracted from session data

    Returns:
        AnalysisResult with comprehensive analysis
    """
    # Generate statistics
    stats = generate_statistics(extracted_commands)

    # Deduplicate
    deduplicated, fuzzy_groups = deduplicate(extracted_commands)

    # Filter to non-fuzzy-duplicates for unique list
    unique_deduplicated = [d for d in deduplicated if not d['is_fuzzy_duplicate']]

    return AnalysisResult(
        total_commands=stats['total_commands'],
        unique_commands=stats['unique_commands'],
        unique_base_commands=stats['unique_base_commands'],
        complexity_distribution=stats['complexity_distribution'],
        category_breakdown=stats['category_breakdown'],
        top_commands=stats['top_commands'],
        top_base_commands=stats['top_base_commands'],
        deduplicated_commands=deduplicated,
        fuzzy_groups=fuzzy_groups,
        statistics=stats,
    )


def format_analysis_report(result: AnalysisResult) -> str:
    """
    Format an analysis result as a human-readable report.

    Args:
        result: AnalysisResult to format

    Returns:
        Formatted string report
    """
    lines = [
        "=" * 60,
        "BASH COMMAND ANALYSIS REPORT",
        "=" * 60,
        "",
        "SUMMARY",
        "-" * 40,
        f"Total commands analyzed: {result.total_commands}",
        f"Unique command strings: {result.unique_commands}",
        f"Unique base utilities: {result.unique_base_commands}",
        f"Average complexity: {result.statistics.get('average_complexity', 0):.2f}",
        "",
        "COMPLEXITY DISTRIBUTION",
        "-" * 40,
    ]

    complexity_labels = {
        1: "Simple (no flags)",
        2: "Basic (with flags)",
        3: "Intermediate (pipes/redirects)",
        4: "Advanced (compound/loops)",
        5: "Expert (complex pipelines)",
    }

    for level in range(1, 6):
        count = result.complexity_distribution.get(level, 0)
        pct = (count / result.total_commands * 100) if result.total_commands else 0
        bar = "#" * int(pct / 2)
        lines.append(f"  {level}: {complexity_labels[level]:<30} {count:>5} ({pct:>5.1f}%) {bar}")

    lines.extend([
        "",
        "CATEGORY BREAKDOWN",
        "-" * 40,
    ])

    for category, count in sorted(result.category_breakdown.items(), key=lambda x: -x[1]):
        pct = (count / result.total_commands * 100) if result.total_commands else 0
        lines.append(f"  {category:<25} {count:>5} ({pct:>5.1f}%)")

    lines.extend([
        "",
        "TOP 10 MOST USED COMMANDS",
        "-" * 40,
    ])

    for cmd, count in result.top_commands[:10]:
        display_cmd = cmd[:50] + "..." if len(cmd) > 50 else cmd
        lines.append(f"  {count:>5}x  {display_cmd}")

    lines.extend([
        "",
        "TOP 10 BASE UTILITIES",
        "-" * 40,
    ])

    for base, count in result.top_base_commands[:10]:
        lines.append(f"  {count:>5}x  {base}")

    if result.statistics.get('most_complex_commands'):
        lines.extend([
            "",
            "MOST COMPLEX COMMANDS (TOP 5)",
            "-" * 40,
        ])
        for cmd, complexity in result.statistics['most_complex_commands'][:5]:
            display_cmd = cmd[:60] + "..." if len(cmd) > 60 else cmd
            lines.append(f"  [Level {complexity}] {display_cmd}")

    lines.extend([
        "",
        "=" * 60,
    ])

    return "\n".join(lines)


# Convenience function for quick analysis
def quick_analyze(commands: List[str], verbose: bool = False) -> Dict[str, Any]:
    """
    Perform a quick analysis and return essential metrics.

    Args:
        commands: List of command strings
        verbose: If True, include full deduplicated list

    Returns:
        Dictionary with analysis summary
    """
    result = analyze_session(commands)

    summary = {
        'total': result.total_commands,
        'unique': result.unique_commands,
        'unique_utilities': result.unique_base_commands,
        'complexity': result.complexity_distribution,
        'categories': result.category_breakdown,
        'top_commands': result.top_commands[:10],
        'top_utilities': result.top_base_commands[:10],
    }

    if verbose:
        summary['deduplicated'] = result.deduplicated_commands
        summary['fuzzy_groups'] = result.fuzzy_groups

    return summary


def analyze_commands(commands: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze a list of command dictionaries for the pipeline.

    This is the interface expected by main.py.

    Args:
        commands: List of command dictionaries with 'command' key

    Returns:
        Dictionary with 'categories', 'commands', 'statistics' keys
    """
    # Extract command strings from dictionaries
    cmd_strings = [
        cmd.get('command', '') or cmd.get('raw', '')
        for cmd in commands
        if cmd.get('command') or cmd.get('raw')
    ]

    if not cmd_strings:
        return {
            'categories': {},
            'commands': [],
            'statistics': {},
        }

    result = analyze_session(cmd_strings)

    # Build analyzed command list with parsed info
    analyzed_commands = []
    for cmd_dict in commands:
        cmd_str = cmd_dict.get('command', '') or cmd_dict.get('raw', '')
        if cmd_str:
            parsed = parse_command(cmd_str)
            analyzed_commands.append({
                'command': cmd_str,
                'description': cmd_dict.get('description', ''),
                'output': cmd_dict.get('output', ''),
                'base_command': parsed.base_command,
                'flags': parsed.flags,
                'args': parsed.args,
                'complexity': score_complexity(parsed),
                'category': assign_category(parsed),
                'success': cmd_dict.get('success', True),
            })

    # Group by category
    categories = {}
    for cmd in analyzed_commands:
        cat = cmd['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(cmd)

    return {
        'categories': categories,
        'commands': analyzed_commands,
        'statistics': result.statistics,
        'category_breakdown': result.category_breakdown,
        'complexity_distribution': result.complexity_distribution,
        'top_commands': result.top_commands,
    }


if __name__ == "__main__":
    # Example usage and testing
    test_commands = [
        "ls",
        "ls -la",
        "ls -la /home/user",
        "cd src",
        "pwd",
        "cat file.txt | grep pattern",
        "find . -name '*.py' | xargs grep 'import'",
        "git status",
        "git commit -m 'test commit'",
        "docker run -it --rm ubuntu bash",
        "for f in *.txt; do echo $f; done",
        "curl -s https://api.example.com | jq '.data'",
        "ps aux | grep python | awk '{print $2}' | xargs kill",
        "npm install",
        "pip install -r requirements.txt",
        "ls -la",  # Duplicate
        "ls -la /home/other",  # Fuzzy duplicate
    ]

    result = analyze_session(test_commands)
    print(format_analysis_report(result))
