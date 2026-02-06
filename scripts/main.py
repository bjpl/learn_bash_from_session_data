#!/usr/bin/env python3
"""
Main orchestration script for learn_bash_from_session_data.

Discovers Claude session files, extracts bash commands, analyzes them,
generates quizzes, and produces HTML learning materials.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Version check
if sys.version_info < (3, 8):
    sys.exit("Error: Python 3.8 or higher is required. Current version: "
             f"{sys.version_info.major}.{sys.version_info.minor}")

# Constants
DEFAULT_OUTPUT_BASE = "./bash-learner-output"
MAX_UNIQUE_COMMANDS = 500
VERSION = "1.1.1"


def generate_timestamped_output_dir(base_dir: str = DEFAULT_OUTPUT_BASE) -> Path:
    """
    Generate a timestamped output directory.

    Args:
        base_dir: Base directory for outputs

    Returns:
        Path to timestamped output directory (e.g., ./bash-learner-output/run-2026-02-05-143052/)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    return Path(base_dir) / f"run-{timestamp}"


def get_sessions_base_path() -> Path:
    """
    Get the base path for Claude session files.

    Handles WSL by checking both Linux and Windows paths.
    """
    # Standard Linux/Mac path
    linux_path = Path.home() / ".claude" / "projects"

    # Check if we're in WSL
    is_wsl = False
    try:
        with open("/proc/version", "r") as f:
            proc_version = f.read().lower()
            is_wsl = "microsoft" in proc_version or "wsl" in proc_version
    except (FileNotFoundError, PermissionError):
        pass

    if is_wsl:
        # Try to find Windows user directory
        # Check common Windows user paths via /mnt/c/Users/
        windows_users = Path("/mnt/c/Users")
        if windows_users.exists():
            # Try current username first
            username = os.environ.get("USER", "")
            windows_path = windows_users / username / ".claude" / "projects"
            if windows_path.exists():
                return windows_path

            # Try to find any user with .claude folder
            for user_dir in windows_users.iterdir():
                if user_dir.is_dir() and not user_dir.name.startswith(("Public", "Default")):
                    potential_path = user_dir / ".claude" / "projects"
                    if potential_path.exists():
                        return potential_path

    # Fall back to Linux path
    return linux_path


SESSIONS_BASE_PATH = get_sessions_base_path()


def get_session_metadata(session_path: Path) -> Dict:
    """
    Extract metadata from a session file.

    Args:
        session_path: Path to the session JSONL file

    Returns:
        Dictionary with session metadata
    """
    stat = session_path.stat()
    mod_time = datetime.fromtimestamp(stat.st_mtime)

    # Try to extract project path hint from parent directory name
    project_hash = session_path.parent.parent.name

    # Try to read first line to get more metadata
    first_message = None
    try:
        with open(session_path, 'r', encoding='utf-8', errors='replace') as f:
            first_line = f.readline().strip()
            if first_line:
                first_message = json.loads(first_line)
    except (json.JSONDecodeError, IOError):
        pass

    return {
        "path": session_path,
        "filename": session_path.name,
        "project_hash": project_hash,
        "size_bytes": stat.st_size,
        "size_human": format_file_size(stat.st_size),
        "modified": mod_time,
        "modified_str": mod_time.strftime("%Y-%m-%d %H:%M:%S"),
        "first_message": first_message,
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def discover_sessions(
    project_filter: Optional[str] = None,
    limit: Optional[int] = None,
    sessions_dir: Optional[Path] = None
) -> List[Dict]:
    """
    Discover available Claude session files.

    Args:
        project_filter: Optional filter for project path substring
        limit: Maximum number of sessions to return
        sessions_dir: Custom sessions directory (defaults to auto-detected)

    Returns:
        List of session metadata dictionaries, sorted by modification time (newest first)
    """
    sessions = []
    base_path = sessions_dir or SESSIONS_BASE_PATH

    if not base_path.exists():
        return sessions

    # Find all session files - check both old and new directory structures
    # New structure: projects/<hash>/sessions/*.jsonl
    # Old structure: projects/<hash>/*.jsonl
    for project_dir in base_path.iterdir():
        if not project_dir.is_dir():
            continue

        # Check for sessions subdirectory (new structure)
        sessions_subdir = project_dir / "sessions"
        if sessions_subdir.exists():
            for session_file in sessions_subdir.glob("*.jsonl"):
                metadata = get_session_metadata(session_file)
                if project_filter and project_filter.lower() not in str(session_file).lower():
                    continue
                sessions.append(metadata)

        # Also check for .jsonl files directly in project dir (old structure)
        for session_file in project_dir.glob("*.jsonl"):
            metadata = get_session_metadata(session_file)

            # Apply project filter if specified
            if project_filter:
                # Check if filter matches project hash or any content
                if project_filter.lower() not in str(session_file).lower():
                    continue

            sessions.append(metadata)

    # Sort by modification time (newest first)
    sessions.sort(key=lambda x: x["modified"], reverse=True)

    if limit:
        sessions = sessions[:limit]

    return sessions


def list_sessions(project_filter: Optional[str] = None, sessions_dir: Optional[Path] = None) -> None:
    """
    Display available sessions in a formatted table.

    Args:
        project_filter: Optional filter for project path substring
        sessions_dir: Custom sessions directory
    """
    base_path = sessions_dir or SESSIONS_BASE_PATH
    sessions = discover_sessions(project_filter=project_filter, sessions_dir=sessions_dir)

    if not sessions:
        print("\nNo session files found.")
        print(f"\nSearched in: {base_path}")
        print(f"\nExpected structure: <sessions-dir>/<project-hash>/*.jsonl")
        print("\nMake sure you have Claude session data available.")
        print("\nTip: On WSL, try using -s /mnt/c/Users/<username>/.claude/projects/")
        return

    print(f"\n{'='*80}")
    print(f"Available Claude Sessions ({len(sessions)} found)")
    print(f"{'='*80}")
    print(f"{'#':<4} {'Date':<20} {'Size':<10} {'Filename':<30}")
    print(f"{'-'*80}")

    for idx, session in enumerate(sessions, 1):
        print(f"{idx:<4} {session['modified_str']:<20} {session['size_human']:<10} "
              f"{session['filename'][:30]:<30}")

    print(f"{'-'*80}")
    print(f"\nUse -n <number> to process the N most recent sessions")
    print(f"Use -f <path> to process a specific session file")


def load_session_file(session_path: Path) -> List[Dict]:
    """
    Load and parse a session JSONL file.

    Args:
        session_path: Path to the session file

    Returns:
        List of parsed JSON objects from the session
    """
    entries = []

    with open(session_path, 'r', encoding='utf-8', errors='replace') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping malformed JSON at line {line_num}: {e}")

    return entries


def run_extraction_pipeline(
    sessions: List[Dict],
    output_dir: Path
) -> Tuple[bool, str]:
    """
    Run the full extraction and generation pipeline.

    Args:
        sessions: List of session metadata dictionaries
        output_dir: Directory for output files

    Returns:
        Tuple of (success: bool, message: str)
    """
    # Import processing modules (lazy import to allow standalone testing)
    try:
        from scripts.extractor import extract_commands
        from scripts.parser import parse_commands
        from scripts.analyzer import analyze_commands
        from scripts.quiz_generator import generate_quizzes
        from scripts.html_generator import generate_html
    except ImportError:
        # Try relative import for when run as script
        try:
            from extractor import extract_commands
            from parser import parse_commands
            from analyzer import analyze_commands
            from quiz_generator import generate_quizzes
            from html_generator import generate_html
        except ImportError as e:
            return False, f"Failed to import processing modules: {e}"

    # Safety check: prevent writing to critical system directories
    output_resolved = output_dir.resolve()
    forbidden_prefixes = ['/etc', '/usr', '/bin', '/sbin', '/lib', '/boot', '/root', '/sys', '/proc']
    for prefix in forbidden_prefixes:
        if str(output_resolved).startswith(prefix):
            return False, f"Safety error: Cannot write to system directory: {output_resolved}"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nProcessing {len(sessions)} session(s)...")
    print(f"Output directory: {output_dir.absolute()}")
    print("-" * 60)

    # Step 1: Load all session data
    all_entries = []
    for session in sessions:
        print(f"Loading: {session['filename']} ({session['size_human']})")
        entries = load_session_file(session['path'])
        all_entries.extend(entries)
        print(f"  -> Loaded {len(entries)} entries")

    if not all_entries:
        return False, "No session entries found in the provided files."

    print(f"\nTotal entries loaded: {len(all_entries)}")

    # Step 2: Extract commands
    print("\nExtracting bash commands...")
    raw_commands = extract_commands(all_entries)
    print(f"  -> Found {len(raw_commands)} raw commands")

    if not raw_commands:
        return False, ("No bash commands found in the session data. "
                      "Try analyzing more sessions with -n <number>.")

    # Step 3: Parse commands
    print("\nParsing commands...")
    parsed_commands = parse_commands(raw_commands)
    print(f"  -> Parsed {len(parsed_commands)} commands")

    # Step 4: Expand compound commands into individual sub-commands
    # Also count operators for tracking
    from collections import Counter
    import re

    operator_frequency = Counter()
    expanded_commands = []

    # Operator patterns to detect
    operator_patterns = {
        '||': r'\|\|',
        '&&': r'&&',
        '|': r'(?<!\|)\|(?!\|)',  # Single pipe, not ||
        '2>&1': r'2>&1',
        '2>/dev/null': r'2>/dev/null',
        '>': r'(?<![2&])>(?!>|&)',  # Single >, not >> or 2> or >&
        '>>': r'>>',
        '<': r'<(?!<)',
    }

    for cmd in parsed_commands:
        cmd_str = cmd.get('command', '') or cmd.get('raw', '')
        if not cmd_str:
            continue

        # Count operators in this command
        for op_name, op_pattern in operator_patterns.items():
            matches = re.findall(op_pattern, cmd_str)
            if matches:
                operator_frequency[op_name] += len(matches)

        # Check if this is a compound command
        is_compound = any(op in cmd_str for op in ['||', '&&', ' | ', ';'])

        if is_compound:
            # Extract individual sub-commands from compound statement
            sub_commands = extract_sub_commands(cmd_str)
            for sub_cmd in sub_commands:
                if sub_cmd.strip():
                    expanded_commands.append({
                        'command': sub_cmd.strip(),
                        'raw': sub_cmd.strip(),
                        'original_compound': cmd_str,
                        'description': cmd.get('description', ''),
                        'output': cmd.get('output', ''),
                    })
        else:
            # Simple command - add as-is
            expanded_commands.append(cmd)

    print(f"  -> Expanded to {len(expanded_commands)} individual commands")

    # Step 5: Re-parse expanded commands to get proper base_command for each
    parsed_expanded = parse_commands(expanded_commands)

    # Step 6: Count frequencies BEFORE deduplication (for accurate usage stats)
    cmd_frequency = Counter()
    base_cmd_frequency = Counter()

    for cmd in parsed_expanded:
        cmd_str = cmd.get('command', '') or cmd.get('raw', '')
        base_cmd = cmd.get('base_command', '')
        if cmd_str:
            cmd_frequency[cmd_str] += 1
        if base_cmd:
            base_cmd_frequency[base_cmd] += 1

    # Step 7: Deduplicate and attach frequency data
    unique_commands = deduplicate_commands(parsed_expanded)

    # Add frequency to each unique command
    for cmd in unique_commands:
        cmd_str = cmd.get('command', '') or cmd.get('raw', '')
        base_cmd = cmd.get('base_command', '')
        cmd['frequency'] = cmd_frequency.get(cmd_str, 1)
        cmd['base_frequency'] = base_cmd_frequency.get(base_cmd, 1)

    if len(unique_commands) > MAX_UNIQUE_COMMANDS:
        print(f"\nCapping at {MAX_UNIQUE_COMMANDS} unique commands "
              f"(found {len(unique_commands)})")
        unique_commands = unique_commands[:MAX_UNIQUE_COMMANDS]
    else:
        print(f"\n{len(unique_commands)} unique commands")

    # Step 8: Analyze commands
    print("\nAnalyzing commands...")
    analysis = analyze_commands(unique_commands)

    # Inject pre-computed frequency data into analysis
    analysis['command_frequency'] = dict(cmd_frequency)
    analysis['base_command_frequency'] = dict(base_cmd_frequency)
    analysis['top_commands'] = cmd_frequency.most_common(20)
    analysis['top_base_commands'] = base_cmd_frequency.most_common(20)
    analysis['operators_used'] = dict(operator_frequency)
    print(f"  -> Generated analysis with {len(analysis.get('categories', {}))} categories")

    # Step 9: Generate quizzes
    print("\nGenerating quizzes...")
    quizzes = generate_quizzes(unique_commands, analysis)
    quiz_count = sum(len(q) for q in quizzes.values()) if isinstance(quizzes, dict) else len(quizzes)
    print(f"  -> Generated {quiz_count} quiz questions")

    # Step 10: Generate HTML
    print("\nGenerating HTML output...")
    html_files = generate_html(unique_commands, analysis, quizzes, output_dir)
    print(f"  -> Created {len(html_files)} HTML files")

    # Write summary JSON with comprehensive metadata
    summary = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "run_id": output_dir.name,
            "version": VERSION,
        },
        "input": {
            "sessions_processed": len(sessions),
            "session_files": [
                {
                    "filename": s['filename'],
                    "path": str(s['path']),
                    "size": s['size_human'],
                    "modified": s['modified_str']
                }
                for s in sessions
            ],
            "total_entries": len(all_entries),
        },
        "analysis": {
            "raw_commands_found": len(raw_commands),
            "unique_commands": len(unique_commands),
            "categories": list(analysis.get('categories', {}).keys()),
            "category_counts": {cat: len(cmds) for cat, cmds in analysis.get('categories', {}).items()},
            "top_base_commands": [
                {"command": cmd, "count": count}
                for cmd, count in list(base_cmd_frequency.most_common(10))
            ],
            "operators_used": dict(operator_frequency),
            "complexity_distribution": dict(analysis.get('complexity_distribution', {})),
        },
        "output": {
            "quiz_questions": quiz_count,
            "html_files": [str(f) for f in html_files],
        },
    }

    summary_path = output_dir / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary written to: {summary_path}")

    return True, f"Successfully generated learning materials in {output_dir}"


def extract_sub_commands(cmd_str: str) -> List[str]:
    """
    Extract individual sub-commands from a compound command.

    Splits commands by ||, &&, |, and ; while respecting quoting
    and skipping inline code commands (python -c, node -e, bash -c).

    Args:
        cmd_str: The compound command string

    Returns:
        List of individual sub-command strings
    """
    import re

    if not cmd_str or not cmd_str.strip():
        return []

    # Don't split commands that contain inline code - the ; and | inside
    # quoted code would produce garbage fragments
    inline_patterns = [' -c "', " -c '", ' -c $', ' -e "', " -e '", ' -e $',
                       ' -c\n', ' -c\r']
    first_token = cmd_str.split()[0] if cmd_str.split() else ''
    if first_token in ('python', 'python3', 'node', 'bash', 'sh', 'ruby', 'perl'):
        for pat in inline_patterns:
            if pat in cmd_str:
                return [cmd_str.strip()]

    # Quote-aware splitting: track quote depth to avoid splitting inside quotes
    sub_commands = []
    current = []
    in_single = False
    in_double = False
    i = 0
    chars = cmd_str

    while i < len(chars):
        c = chars[i]

        # Track quoting state
        if c == "'" and not in_double:
            in_single = not in_single
            current.append(c)
            i += 1
        elif c == '"' and not in_single:
            in_double = not in_double
            current.append(c)
            i += 1
        elif not in_single and not in_double:
            # Check for compound operators outside quotes
            remaining = chars[i:]
            if remaining.startswith('&&'):
                cmd = ''.join(current).strip()
                if cmd:
                    sub_commands.append(cmd)
                current = []
                i += 2
            elif remaining.startswith('||'):
                cmd = ''.join(current).strip()
                if cmd:
                    sub_commands.append(cmd)
                current = []
                i += 2
            elif c == ';':
                cmd = ''.join(current).strip()
                if cmd:
                    sub_commands.append(cmd)
                current = []
                i += 1
            elif c == '|' and not remaining.startswith('||'):
                cmd = ''.join(current).strip()
                if cmd:
                    sub_commands.append(cmd)
                current = []
                i += 1
            else:
                current.append(c)
                i += 1
        else:
            current.append(c)
            i += 1

    # Add final segment
    cmd = ''.join(current).strip()
    if cmd:
        sub_commands.append(cmd)

    return sub_commands


def deduplicate_commands(commands: List[Dict]) -> List[Dict]:
    """
    Remove duplicate commands while preserving order.

    Args:
        commands: List of parsed command dictionaries

    Returns:
        Deduplicated list of commands
    """
    seen = set()
    unique = []

    for cmd in commands:
        # Create a key based on the command string
        key = cmd.get('command', '') or cmd.get('raw', '')
        if key and key not in seen:
            seen.add(key)
            unique.append(cmd)

    return unique


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Learn Bash from Claude session data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    List available sessions
  %(prog)s -n 5                      Process 5 most recent sessions
  %(prog)s -f /path/to/session.jsonl Process specific session file
  %(prog)s -n 10 -o ./my-output/     Process 10 sessions to custom directory
  %(prog)s -l -p myproject           List sessions matching 'myproject'
        """
    )

    parser.add_argument(
        '-n', '--sessions',
        type=int,
        default=1,
        help='Number of recent sessions to process (default: 1)'
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Specific session file path to process'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help=f'Output directory (default: timestamped folder in {DEFAULT_OUTPUT_BASE}/)'
    )

    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available sessions'
    )

    parser.add_argument(
        '-p', '--project',
        type=str,
        help='Filter sessions by project path substring'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '-s', '--sessions-dir',
        type=str,
        help=f'Sessions directory (default: auto-detected, currently {SESSIONS_BASE_PATH})'
    )

    return parser.parse_args()


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    args = parse_arguments()

    # Handle custom sessions directory
    custom_sessions_dir = Path(args.sessions_dir) if args.sessions_dir else None

    # Handle --list
    if args.list:
        list_sessions(project_filter=args.project, sessions_dir=custom_sessions_dir)
        return 0

    # Determine which sessions to process
    sessions_to_process = []

    if args.file:
        # Process specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: Session file not found: {args.file}")
            return 1
        if not file_path.suffix == '.jsonl':
            print(f"Warning: Expected .jsonl file, got: {file_path.suffix}")

        sessions_to_process = [get_session_metadata(file_path)]

    else:
        # Discover and select sessions
        base_path = custom_sessions_dir or SESSIONS_BASE_PATH
        sessions = discover_sessions(
            project_filter=args.project,
            limit=args.sessions,
            sessions_dir=custom_sessions_dir
        )

        if not sessions:
            print("\nNo session files found.")
            print(f"\nSearched in: {base_path}")
            print(f"\nExpected structure: <sessions-dir>/<project-hash>/*.jsonl")
            print("\nTo create session data, use Claude Code and your sessions will be stored automatically.")
            print("\nUse --list to see available sessions once you have some.")
            print("\nTip: On WSL, try using -s /mnt/c/Users/<username>/.claude/projects/")
            return 1

        sessions_to_process = sessions

    # Run the pipeline with timestamped output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = generate_timestamped_output_dir()
    success, message = run_extraction_pipeline(sessions_to_process, output_dir)

    if success:
        print(f"\n{'='*60}")
        print("SUCCESS!")
        print(message)
        print(f"{'='*60}")

        # Print next steps
        index_file = output_dir / "index.html"
        if index_file.exists():
            print(f"\nOpen {index_file.absolute()} in your browser to start learning!")

        return 0
    else:
        print(f"\nError: {message}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
