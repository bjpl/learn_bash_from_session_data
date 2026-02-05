"""
JSONL Extractor for Claude Code Session Data

Parses JSONL files from Claude Code sessions, extracts bash tool_use events,
and correlates them with their corresponding tool_result outputs.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class ExtractedCommand:
    """Represents an extracted bash command from a Claude Code session."""
    command: str
    description: str
    output: str
    timestamp: str
    sequence_number: int
    tool_use_id: str = ""
    success: bool = True
    exit_code: Optional[int] = None


class JSONLExtractor:
    """
    Extracts bash commands from Claude Code session JSONL files.

    Claude Code sessions store tool interactions in JSONL format with:
    - tool_use blocks containing the command and description
    - tool_result blocks containing the execution output

    This extractor correlates tool_use with tool_result by matching tool_use_id.
    """

    def __init__(self, session_path: Optional[Path] = None):
        """
        Initialize the extractor.

        Args:
            session_path: Optional path to Claude Code sessions directory.
                         Defaults to ~/.claude/projects/
        """
        if session_path is None:
            home = Path.home()
            session_path = home / ".claude" / "projects"
        self.session_path = Path(session_path)

    def find_session_files(self, project_filter: Optional[str] = None) -> Iterator[Path]:
        """
        Find all JSONL session files.

        Args:
            project_filter: Optional substring to filter project directories

        Yields:
            Paths to JSONL files
        """
        if not self.session_path.exists():
            return

        for project_dir in self.session_path.iterdir():
            if not project_dir.is_dir():
                continue
            if project_filter and project_filter not in project_dir.name:
                continue

            # Look for JSONL files in project directory and subdirectories
            for jsonl_file in project_dir.rglob("*.jsonl"):
                yield jsonl_file

    def extract_from_file(self, file_path: Path) -> list[ExtractedCommand]:
        """
        Extract bash commands from a single JSONL file.

        Args:
            file_path: Path to the JSONL file

        Returns:
            List of ExtractedCommand objects
        """
        tool_uses: dict[str, dict] = {}  # tool_use_id -> tool_use data
        tool_results: dict[str, dict] = {}  # tool_use_id -> tool_result data
        sequence_counter = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract tool_use and tool_result from various message formats
                self._process_entry(entry, tool_uses, tool_results, sequence_counter)
                sequence_counter += 1

        # Correlate tool_use with tool_result
        return self._correlate_commands(tool_uses, tool_results)

    def _process_entry(
        self,
        entry: dict,
        tool_uses: dict,
        tool_results: dict,
        sequence: int
    ) -> None:
        """
        Process a single JSONL entry to extract tool_use and tool_result blocks.

        Handles multiple message formats from Claude Code sessions:
        - Direct content arrays
        - Nested message structures
        - Assistant/user message pairs
        """
        # Handle direct content array format
        if isinstance(entry, dict) and 'content' in entry:
            content = entry.get('content', [])
            if isinstance(content, list):
                for block in content:
                    self._process_content_block(block, tool_uses, tool_results, sequence, entry)
            elif isinstance(content, str):
                # Text-only content, skip
                pass

        # Handle message format with role
        if isinstance(entry, dict) and 'message' in entry:
            message = entry['message']
            if isinstance(message, dict) and 'content' in message:
                content = message.get('content', [])
                if isinstance(content, list):
                    for block in content:
                        self._process_content_block(block, tool_uses, tool_results, sequence, entry)

        # Handle nested messages array
        if isinstance(entry, dict) and 'messages' in entry:
            for msg in entry.get('messages', []):
                if isinstance(msg, dict) and 'content' in msg:
                    content = msg.get('content', [])
                    if isinstance(content, list):
                        for block in content:
                            self._process_content_block(block, tool_uses, tool_results, sequence, entry)

    def _process_content_block(
        self,
        block: dict,
        tool_uses: dict,
        tool_results: dict,
        sequence: int,
        parent_entry: dict
    ) -> None:
        """Process a single content block for tool_use or tool_result."""
        if not isinstance(block, dict):
            return

        block_type = block.get('type', '')

        if block_type == 'tool_use':
            tool_name = block.get('name', '')
            if tool_name.lower() == 'bash' or tool_name == 'Bash':
                tool_use_id = block.get('id', '')
                input_data = block.get('input', {})

                # Extract command and description
                command = ''
                description = ''

                if isinstance(input_data, dict):
                    command = input_data.get('command', '')
                    description = input_data.get('description', '')
                elif isinstance(input_data, str):
                    command = input_data

                if command and tool_use_id:
                    # Extract timestamp from parent entry
                    timestamp = self._extract_timestamp(parent_entry)

                    tool_uses[tool_use_id] = {
                        'command': command,
                        'description': description or '',
                        'timestamp': timestamp,
                        'sequence': sequence
                    }

        elif block_type == 'tool_result':
            tool_use_id = block.get('tool_use_id', '')
            if tool_use_id:
                content = block.get('content', '')

                # Handle content that might be a list of text blocks
                if isinstance(content, list):
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text_parts.append(item.get('text', ''))
                        elif isinstance(item, str):
                            text_parts.append(item)
                    content = '\n'.join(text_parts)

                # Check for error indicators
                is_error = block.get('is_error', False)

                tool_results[tool_use_id] = {
                    'output': content,
                    'is_error': is_error
                }

    def _extract_timestamp(self, entry: dict) -> str:
        """Extract timestamp from entry, trying multiple possible locations."""
        # Try common timestamp field names
        for field in ['timestamp', 'created_at', 'time', 'ts', 'datetime']:
            if field in entry:
                return str(entry[field])

        # Try nested message timestamp
        if 'message' in entry and isinstance(entry['message'], dict):
            for field in ['timestamp', 'created_at', 'time']:
                if field in entry['message']:
                    return str(entry['message'][field])

        return ''

    def _correlate_commands(
        self,
        tool_uses: dict,
        tool_results: dict
    ) -> list[ExtractedCommand]:
        """
        Correlate tool_use blocks with their corresponding tool_result blocks.

        Args:
            tool_uses: Dict mapping tool_use_id to tool_use data
            tool_results: Dict mapping tool_use_id to tool_result data

        Returns:
            List of ExtractedCommand objects, sorted by sequence number
        """
        commands = []

        for tool_use_id, use_data in tool_uses.items():
            result_data = tool_results.get(tool_use_id, {})

            output = result_data.get('output', '')
            is_error = result_data.get('is_error', False)

            # Try to extract exit code from output if present
            exit_code = self._extract_exit_code(output)

            cmd = ExtractedCommand(
                command=use_data['command'],
                description=use_data['description'],
                output=output,
                timestamp=use_data['timestamp'],
                sequence_number=use_data['sequence'],
                tool_use_id=tool_use_id,
                success=not is_error and (exit_code is None or exit_code == 0),
                exit_code=exit_code
            )
            commands.append(cmd)

        # Sort by sequence number to maintain order
        commands.sort(key=lambda x: x.sequence_number)
        return commands

    def _extract_exit_code(self, output: str) -> Optional[int]:
        """
        Try to extract exit code from command output.

        Some outputs include exit code information in various formats.
        """
        if not output:
            return None

        # Common patterns for exit codes in output
        import re

        patterns = [
            r'exit code[:\s]+(\d+)',
            r'exited with[:\s]+(\d+)',
            r'return code[:\s]+(\d+)',
            r'\[exit code: (\d+)\]',
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass

        return None

    def extract_all(
        self,
        project_filter: Optional[str] = None
    ) -> list[ExtractedCommand]:
        """
        Extract bash commands from all session files.

        Args:
            project_filter: Optional substring to filter project directories

        Returns:
            List of all ExtractedCommand objects from all files
        """
        all_commands = []

        for file_path in self.find_session_files(project_filter):
            try:
                commands = self.extract_from_file(file_path)
                all_commands.extend(commands)
            except (IOError, OSError) as e:
                # Log error but continue processing other files
                print(f"Warning: Could not process {file_path}: {e}")

        return all_commands

    def extract_from_directory(self, directory: Path) -> list[ExtractedCommand]:
        """
        Extract bash commands from all JSONL files in a directory.

        Args:
            directory: Path to directory containing JSONL files

        Returns:
            List of ExtractedCommand objects
        """
        all_commands = []
        directory = Path(directory)

        if not directory.exists():
            return all_commands

        for jsonl_file in directory.rglob("*.jsonl"):
            try:
                commands = self.extract_from_file(jsonl_file)
                all_commands.extend(commands)
            except (IOError, OSError) as e:
                print(f"Warning: Could not process {jsonl_file}: {e}")

        return all_commands


def extract_commands(entries: list[dict]) -> list[dict]:
    """
    Extract bash commands from a list of session entries.

    This is the interface expected by main.py for pipeline processing.

    Args:
        entries: List of parsed JSON entries from session files

    Returns:
        List of command dictionaries with 'command', 'description', 'output' keys
    """
    extractor = JSONLExtractor()
    tool_uses: dict[str, dict] = {}
    tool_results: dict[str, dict] = {}
    sequence_counter = 0

    for entry in entries:
        extractor._process_entry(entry, tool_uses, tool_results, sequence_counter)
        sequence_counter += 1

    extracted = extractor._correlate_commands(tool_uses, tool_results)

    # Convert ExtractedCommand objects to dicts for pipeline compatibility
    return [
        {
            'command': cmd.command,
            'description': cmd.description,
            'output': cmd.output,
            'timestamp': cmd.timestamp,
            'success': cmd.success,
            'exit_code': cmd.exit_code,
        }
        for cmd in extracted
    ]


def extract_commands_from_jsonl(file_path: str | Path) -> list[ExtractedCommand]:
    """
    Convenience function to extract commands from a single JSONL file.

    Args:
        file_path: Path to the JSONL file

    Returns:
        List of ExtractedCommand objects
    """
    extractor = JSONLExtractor()
    return extractor.extract_from_file(Path(file_path))


def extract_commands_from_sessions(
    session_path: Optional[str | Path] = None,
    project_filter: Optional[str] = None
) -> list[ExtractedCommand]:
    """
    Convenience function to extract commands from Claude Code session files.

    Args:
        session_path: Path to sessions directory (defaults to ~/.claude/projects/)
        project_filter: Optional substring to filter project directories

    Returns:
        List of ExtractedCommand objects
    """
    path = Path(session_path) if session_path else None
    extractor = JSONLExtractor(path)
    return extractor.extract_all(project_filter)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Process specific file or directory
        target = Path(sys.argv[1])
        extractor = JSONLExtractor()

        if target.is_file():
            commands = extractor.extract_from_file(target)
        elif target.is_dir():
            commands = extractor.extract_from_directory(target)
        else:
            print(f"Error: {target} is not a valid file or directory")
            sys.exit(1)
    else:
        # Process all session files
        extractor = JSONLExtractor()
        commands = extractor.extract_all()

    print(f"Extracted {len(commands)} bash commands")

    for i, cmd in enumerate(commands[:10], 1):
        print(f"\n--- Command {i} ---")
        print(f"Command: {cmd.command[:100]}{'...' if len(cmd.command) > 100 else ''}")
        print(f"Description: {cmd.description[:80]}{'...' if len(cmd.description) > 80 else ''}")
        print(f"Output length: {len(cmd.output)} chars")
        print(f"Success: {cmd.success}")
