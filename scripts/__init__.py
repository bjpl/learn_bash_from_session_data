"""
Scripts package for learn_bash_from_session_data.

Provides JSONL extraction and bash command parsing utilities.
"""

from .extractor import (
    ExtractedCommand,
    JSONLExtractor,
    extract_commands_from_jsonl,
    extract_commands_from_sessions,
)

from .parser import (
    ParsedCommand,
    CommandCategory,
    BashParser,
    parse_command,
    parse_commands,
)

__all__ = [
    # Extractor
    "ExtractedCommand",
    "JSONLExtractor",
    "extract_commands_from_jsonl",
    "extract_commands_from_sessions",
    # Parser
    "ParsedCommand",
    "CommandCategory",
    "BashParser",
    "parse_command",
    "parse_commands",
]
