"""
Bash Command Parser

Parses bash commands using shlex tokenization and regex patterns to extract
structural information like pipes, redirects, subshells, and variables.
"""

import re
import shlex
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class CommandCategory(Enum):
    """Categories for bash commands based on their primary purpose."""
    FILE_OPERATION = "file_operation"
    DIRECTORY = "directory"
    TEXT_PROCESSING = "text_processing"
    SEARCH = "search"
    VERSION_CONTROL = "version_control"
    PACKAGE_MANAGEMENT = "package_management"
    PROCESS_MANAGEMENT = "process_management"
    NETWORK = "network"
    SYSTEM_INFO = "system_info"
    PERMISSION = "permission"
    ARCHIVE = "archive"
    ENVIRONMENT = "environment"
    BUILD = "build"
    TESTING = "testing"
    DOCKER = "docker"
    UNKNOWN = "unknown"


@dataclass
class ParsedCommand:
    """Represents a fully parsed bash command with structural analysis."""
    raw: str
    description: str
    base_commands: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    pipes: list[str] = field(default_factory=list)
    redirects: list[dict] = field(default_factory=list)
    subshells: list[str] = field(default_factory=list)
    variables: list[dict] = field(default_factory=list)
    logical_ops: list[str] = field(default_factory=list)
    output: str = ""
    complexity_score: int = 0
    category: CommandCategory = CommandCategory.UNKNOWN
    arguments: list[str] = field(default_factory=list)
    is_multiline: bool = False
    has_heredoc: bool = False
    parse_errors: list[str] = field(default_factory=list)


class BashParser:
    """
    Parser for bash commands that extracts structural information.

    Uses shlex for tokenization and regex patterns for detecting
    bash-specific constructs like pipes, redirects, and subshells.
    """

    # Command categorization mapping
    COMMAND_CATEGORIES = {
        # File operations
        'cat': CommandCategory.FILE_OPERATION,
        'head': CommandCategory.FILE_OPERATION,
        'tail': CommandCategory.FILE_OPERATION,
        'cp': CommandCategory.FILE_OPERATION,
        'mv': CommandCategory.FILE_OPERATION,
        'rm': CommandCategory.FILE_OPERATION,
        'touch': CommandCategory.FILE_OPERATION,
        'ln': CommandCategory.FILE_OPERATION,
        'file': CommandCategory.FILE_OPERATION,
        'stat': CommandCategory.FILE_OPERATION,
        'wc': CommandCategory.FILE_OPERATION,
        'diff': CommandCategory.FILE_OPERATION,
        'patch': CommandCategory.FILE_OPERATION,

        # Directory operations
        'ls': CommandCategory.DIRECTORY,
        'cd': CommandCategory.DIRECTORY,
        'pwd': CommandCategory.DIRECTORY,
        'mkdir': CommandCategory.DIRECTORY,
        'rmdir': CommandCategory.DIRECTORY,
        'tree': CommandCategory.DIRECTORY,
        'find': CommandCategory.DIRECTORY,
        'locate': CommandCategory.DIRECTORY,

        # Text processing
        'grep': CommandCategory.TEXT_PROCESSING,
        'sed': CommandCategory.TEXT_PROCESSING,
        'awk': CommandCategory.TEXT_PROCESSING,
        'cut': CommandCategory.TEXT_PROCESSING,
        'sort': CommandCategory.TEXT_PROCESSING,
        'uniq': CommandCategory.TEXT_PROCESSING,
        'tr': CommandCategory.TEXT_PROCESSING,
        'xargs': CommandCategory.TEXT_PROCESSING,
        'tee': CommandCategory.TEXT_PROCESSING,
        'paste': CommandCategory.TEXT_PROCESSING,
        'column': CommandCategory.TEXT_PROCESSING,
        'jq': CommandCategory.TEXT_PROCESSING,
        'yq': CommandCategory.TEXT_PROCESSING,

        # Search
        'rg': CommandCategory.SEARCH,
        'ag': CommandCategory.SEARCH,
        'fzf': CommandCategory.SEARCH,
        'fd': CommandCategory.SEARCH,

        # Version control
        'git': CommandCategory.VERSION_CONTROL,
        'gh': CommandCategory.VERSION_CONTROL,
        'svn': CommandCategory.VERSION_CONTROL,
        'hg': CommandCategory.VERSION_CONTROL,

        # Package management
        'npm': CommandCategory.PACKAGE_MANAGEMENT,
        'npx': CommandCategory.PACKAGE_MANAGEMENT,
        'yarn': CommandCategory.PACKAGE_MANAGEMENT,
        'pnpm': CommandCategory.PACKAGE_MANAGEMENT,
        'pip': CommandCategory.PACKAGE_MANAGEMENT,
        'pip3': CommandCategory.PACKAGE_MANAGEMENT,
        'pipx': CommandCategory.PACKAGE_MANAGEMENT,
        'apt': CommandCategory.PACKAGE_MANAGEMENT,
        'apt-get': CommandCategory.PACKAGE_MANAGEMENT,
        'brew': CommandCategory.PACKAGE_MANAGEMENT,
        'cargo': CommandCategory.PACKAGE_MANAGEMENT,
        'go': CommandCategory.PACKAGE_MANAGEMENT,

        # Process management
        'ps': CommandCategory.PROCESS_MANAGEMENT,
        'top': CommandCategory.PROCESS_MANAGEMENT,
        'htop': CommandCategory.PROCESS_MANAGEMENT,
        'kill': CommandCategory.PROCESS_MANAGEMENT,
        'pkill': CommandCategory.PROCESS_MANAGEMENT,
        'pgrep': CommandCategory.PROCESS_MANAGEMENT,
        'bg': CommandCategory.PROCESS_MANAGEMENT,
        'fg': CommandCategory.PROCESS_MANAGEMENT,
        'jobs': CommandCategory.PROCESS_MANAGEMENT,
        'nohup': CommandCategory.PROCESS_MANAGEMENT,
        'timeout': CommandCategory.PROCESS_MANAGEMENT,
        'watch': CommandCategory.PROCESS_MANAGEMENT,

        # Network
        'curl': CommandCategory.NETWORK,
        'wget': CommandCategory.NETWORK,
        'ssh': CommandCategory.NETWORK,
        'scp': CommandCategory.NETWORK,
        'rsync': CommandCategory.NETWORK,
        'ping': CommandCategory.NETWORK,
        'netstat': CommandCategory.NETWORK,
        'nc': CommandCategory.NETWORK,
        'nmap': CommandCategory.NETWORK,
        'ifconfig': CommandCategory.NETWORK,
        'ip': CommandCategory.NETWORK,

        # System info
        'uname': CommandCategory.SYSTEM_INFO,
        'whoami': CommandCategory.SYSTEM_INFO,
        'hostname': CommandCategory.SYSTEM_INFO,
        'df': CommandCategory.SYSTEM_INFO,
        'du': CommandCategory.SYSTEM_INFO,
        'free': CommandCategory.SYSTEM_INFO,
        'uptime': CommandCategory.SYSTEM_INFO,
        'date': CommandCategory.SYSTEM_INFO,
        'cal': CommandCategory.SYSTEM_INFO,
        'env': CommandCategory.SYSTEM_INFO,
        'printenv': CommandCategory.SYSTEM_INFO,
        'which': CommandCategory.SYSTEM_INFO,
        'whereis': CommandCategory.SYSTEM_INFO,
        'type': CommandCategory.SYSTEM_INFO,
        'man': CommandCategory.SYSTEM_INFO,
        'help': CommandCategory.SYSTEM_INFO,

        # Permissions
        'chmod': CommandCategory.PERMISSION,
        'chown': CommandCategory.PERMISSION,
        'chgrp': CommandCategory.PERMISSION,
        'sudo': CommandCategory.PERMISSION,
        'su': CommandCategory.PERMISSION,

        # Archive
        'tar': CommandCategory.ARCHIVE,
        'zip': CommandCategory.ARCHIVE,
        'unzip': CommandCategory.ARCHIVE,
        'gzip': CommandCategory.ARCHIVE,
        'gunzip': CommandCategory.ARCHIVE,
        'bzip2': CommandCategory.ARCHIVE,
        'xz': CommandCategory.ARCHIVE,
        '7z': CommandCategory.ARCHIVE,

        # Environment
        'export': CommandCategory.ENVIRONMENT,
        'source': CommandCategory.ENVIRONMENT,
        'alias': CommandCategory.ENVIRONMENT,
        'unalias': CommandCategory.ENVIRONMENT,
        'set': CommandCategory.ENVIRONMENT,
        'unset': CommandCategory.ENVIRONMENT,
        'eval': CommandCategory.ENVIRONMENT,

        # Build
        'make': CommandCategory.BUILD,
        'cmake': CommandCategory.BUILD,
        'gcc': CommandCategory.BUILD,
        'g++': CommandCategory.BUILD,
        'clang': CommandCategory.BUILD,
        'rustc': CommandCategory.BUILD,
        'tsc': CommandCategory.BUILD,
        'node': CommandCategory.BUILD,
        'python': CommandCategory.BUILD,
        'python3': CommandCategory.BUILD,
        'ruby': CommandCategory.BUILD,

        # Testing
        'pytest': CommandCategory.TESTING,
        'jest': CommandCategory.TESTING,
        'mocha': CommandCategory.TESTING,
        'vitest': CommandCategory.TESTING,
        'test': CommandCategory.TESTING,

        # Docker
        'docker': CommandCategory.DOCKER,
        'docker-compose': CommandCategory.DOCKER,
        'podman': CommandCategory.DOCKER,
        'kubectl': CommandCategory.DOCKER,
    }

    # Regex patterns for bash constructs
    PIPE_PATTERN = re.compile(r'(?<![|])\|(?![|])')
    REDIRECT_PATTERN = re.compile(
        r'(\d*)(>>|>&|&>|2>&1|2>|>|<)'
        r'\s*([^\s&|;<>]+)?'
    )
    SUBSHELL_DOLLAR_PATTERN = re.compile(r'\$\(([^)]+)\)')
    SUBSHELL_BACKTICK_PATTERN = re.compile(r'`([^`]+)`')
    VARIABLE_ASSIGN_PATTERN = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$')
    VARIABLE_REF_PATTERN = re.compile(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?')
    LOGICAL_AND_PATTERN = re.compile(r'&&')
    LOGICAL_OR_PATTERN = re.compile(r'\|\|')
    HEREDOC_PATTERN = re.compile(r'<<-?\s*[\'"]?(\w+)[\'"]?')
    FLAG_PATTERN = re.compile(r'^-{1,2}[A-Za-z0-9][-A-Za-z0-9_=]*$')

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse(self, command: str, description: str = "", output: str = "") -> ParsedCommand:
        """
        Parse a bash command into structural components.

        Args:
            command: The raw bash command string
            description: Optional description of the command
            output: Optional output from command execution

        Returns:
            ParsedCommand object with extracted structural information
        """
        result = ParsedCommand(
            raw=command,
            description=description,
            output=output
        )

        # Check for multiline and heredoc
        result.is_multiline = '\n' in command or '\\' in command
        result.has_heredoc = bool(self.HEREDOC_PATTERN.search(command))

        # Extract subshells first (before tokenization might fail on them)
        result.subshells = self._extract_subshells(command)

        # Extract redirects
        result.redirects = self._extract_redirects(command)

        # Extract variable assignments and references
        result.variables = self._extract_variables(command)

        # Extract logical operators
        result.logical_ops = self._extract_logical_ops(command)

        # Extract pipes and their commands
        result.pipes = self._extract_pipes(command)

        # Tokenize and extract base commands, flags, and arguments
        self._tokenize_and_extract(command, result)

        # Categorize the command
        result.category = self._categorize(result)

        # Calculate complexity score
        result.complexity_score = self._calculate_complexity(result)

        return result

    def _extract_subshells(self, command: str) -> list[str]:
        """Extract subshell expressions from command."""
        subshells = []

        # Find $(...) subshells
        for match in self.SUBSHELL_DOLLAR_PATTERN.finditer(command):
            subshells.append(match.group(1))

        # Find `...` subshells
        for match in self.SUBSHELL_BACKTICK_PATTERN.finditer(command):
            subshells.append(match.group(1))

        return subshells

    def _extract_redirects(self, command: str) -> list[dict]:
        """Extract redirect operations from command."""
        redirects = []

        for match in self.REDIRECT_PATTERN.finditer(command):
            fd = match.group(1) or ''
            operator = match.group(2)
            target = match.group(3) or ''

            redirect_type = 'unknown'
            if operator in ('>', '>>'):
                redirect_type = 'stdout'
            elif operator == '2>':
                redirect_type = 'stderr'
            elif operator in ('>&', '&>', '2>&1'):
                redirect_type = 'both'
            elif operator == '<':
                redirect_type = 'stdin'

            redirects.append({
                'fd': fd,
                'operator': operator,
                'target': target,
                'type': redirect_type
            })

        return redirects

    def _extract_variables(self, command: str) -> list[dict]:
        """Extract variable assignments and references from command."""
        variables = []
        seen_assignments = set()
        seen_references = set()

        # Split by logical operators and pipes to find assignments
        segments = re.split(r'[|&;]', command)

        for segment in segments:
            segment = segment.strip()
            # Check for variable assignment at start of segment
            match = self.VARIABLE_ASSIGN_PATTERN.match(segment)
            if match:
                var_name = match.group(1)
                var_value = match.group(2)
                if var_name not in seen_assignments:
                    variables.append({
                        'name': var_name,
                        'value': var_value,
                        'type': 'assignment'
                    })
                    seen_assignments.add(var_name)

        # Find variable references
        for match in self.VARIABLE_REF_PATTERN.finditer(command):
            var_name = match.group(1)
            if var_name not in seen_references and var_name not in seen_assignments:
                variables.append({
                    'name': var_name,
                    'type': 'reference'
                })
                seen_references.add(var_name)

        return variables

    def _extract_logical_ops(self, command: str) -> list[str]:
        """Extract logical operators (&&, ||) from command."""
        ops = []

        for match in self.LOGICAL_AND_PATTERN.finditer(command):
            ops.append('&&')

        for match in self.LOGICAL_OR_PATTERN.finditer(command):
            ops.append('||')

        return ops

    def _extract_pipes(self, command: str) -> list[str]:
        """Extract piped command segments."""
        # Remove subshells temporarily to avoid false positives
        temp_cmd = self.SUBSHELL_DOLLAR_PATTERN.sub('__SUBSHELL__', command)
        temp_cmd = self.SUBSHELL_BACKTICK_PATTERN.sub('__SUBSHELL__', temp_cmd)

        # Split by single pipes (not ||)
        segments = self.PIPE_PATTERN.split(temp_cmd)

        if len(segments) <= 1:
            return []

        # Clean up segments
        pipes = []
        for seg in segments:
            seg = seg.strip()
            if seg and seg != '__SUBSHELL__':
                pipes.append(seg)

        return pipes

    def _tokenize_and_extract(self, command: str, result: ParsedCommand) -> None:
        """
        Tokenize command and extract base commands, flags, and arguments.

        Uses shlex for safe tokenization, with fallback for unparseable commands.
        """
        # Prepare command for tokenization
        # Remove heredocs which break shlex
        tokenize_cmd = self.HEREDOC_PATTERN.sub('', command)

        # Replace subshells with placeholders
        tokenize_cmd = self.SUBSHELL_DOLLAR_PATTERN.sub('__SUBSHELL__', tokenize_cmd)
        tokenize_cmd = self.SUBSHELL_BACKTICK_PATTERN.sub('__SUBSHELL__', tokenize_cmd)

        try:
            # Use shlex for tokenization
            lexer = shlex.shlex(tokenize_cmd, posix=True)
            lexer.whitespace_split = True
            lexer.commenters = ''  # Don't treat # as comment for first pass

            tokens = list(lexer)
        except ValueError as e:
            # shlex couldn't parse (unclosed quotes, etc.)
            result.parse_errors.append(f"Tokenization error: {e}")
            # Fallback: simple split
            tokens = tokenize_cmd.split()

        # Process tokens
        base_commands_set = set()
        in_command_position = True
        skip_next = False

        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            # Skip operators
            if token in ('&&', '||', '|', ';', '&'):
                in_command_position = True
                continue

            # Skip redirects
            if token in ('>', '>>', '<', '2>', '2>&1', '>&', '&>'):
                skip_next = True
                continue

            # Skip redirect targets
            if i > 0 and tokens[i-1] in ('>', '>>', '<', '2>', '>&', '&>'):
                continue

            # Skip placeholders
            if token == '__SUBSHELL__':
                continue

            # Check for variable assignment
            if '=' in token and not token.startswith('-'):
                match = self.VARIABLE_ASSIGN_PATTERN.match(token)
                if match:
                    continue

            # Check if it's a flag
            if self.FLAG_PATTERN.match(token):
                result.flags.append(token)
                continue

            # Check if it's a base command
            if in_command_position and not token.startswith('/'):
                # Handle path-prefixed commands
                cmd_name = token.split('/')[-1] if '/' in token else token
                base_commands_set.add(cmd_name)
                in_command_position = False
            else:
                # It's an argument
                if not token.startswith('-'):
                    result.arguments.append(token)

        result.base_commands = list(base_commands_set)

    def _categorize(self, result: ParsedCommand) -> CommandCategory:
        """Determine the category of the command based on base commands."""
        for cmd in result.base_commands:
            if cmd in self.COMMAND_CATEGORIES:
                return self.COMMAND_CATEGORIES[cmd]

        return CommandCategory.UNKNOWN

    def _calculate_complexity(self, result: ParsedCommand) -> int:
        """
        Calculate a complexity score for the command.

        Higher scores indicate more complex commands.
        """
        score = 0

        # Base complexity
        score += len(result.base_commands)

        # Flags add complexity
        score += len(result.flags) * 0.5

        # Pipes add significant complexity
        score += len(result.pipes) * 2

        # Redirects add moderate complexity
        score += len(result.redirects) * 1.5

        # Subshells add significant complexity
        score += len(result.subshells) * 3

        # Logical operators add complexity
        score += len(result.logical_ops) * 1.5

        # Variables add some complexity
        score += len(result.variables)

        # Multiline commands are more complex
        if result.is_multiline:
            score += 2

        # Heredocs are complex
        if result.has_heredoc:
            score += 3

        # Arguments add minor complexity
        score += len(result.arguments) * 0.25

        return int(round(score))

    def parse_batch(
        self,
        commands: list[tuple[str, str, str]]
    ) -> list[ParsedCommand]:
        """
        Parse multiple commands.

        Args:
            commands: List of (command, description, output) tuples

        Returns:
            List of ParsedCommand objects
        """
        return [
            self.parse(cmd, desc, out)
            for cmd, desc, out in commands
        ]


def parse_command(
    command: str,
    description: str = "",
    output: str = ""
) -> ParsedCommand:
    """
    Convenience function to parse a single bash command.

    Args:
        command: The raw bash command string
        description: Optional description
        output: Optional command output

    Returns:
        ParsedCommand object
    """
    parser = BashParser()
    return parser.parse(command, description, output)


def parse_commands(
    commands: list[tuple[str, str, str]]
) -> list[ParsedCommand]:
    """
    Convenience function to parse multiple bash commands.

    Args:
        commands: List of (command, description, output) tuples

    Returns:
        List of ParsedCommand objects
    """
    parser = BashParser()
    return parser.parse_batch(commands)


if __name__ == "__main__":
    # Example usage and testing
    test_commands = [
        ("ls -la /tmp", "List files in tmp", ""),
        ("cat file.txt | grep 'pattern' | sort -u", "Search and sort", ""),
        ("git status && git add . && git commit -m 'test'", "Git workflow", ""),
        ("export FOO=bar && echo $FOO", "Set and use variable", "bar"),
        ("find . -name '*.py' -exec grep -l 'import' {} \\;", "Find Python imports", ""),
        ("docker run -d --name test -p 8080:80 nginx:latest", "Run Docker container", ""),
        ("curl -s https://api.example.com | jq '.data[]'", "API request with jq", ""),
        ("cat <<EOF > output.txt\nline1\nline2\nEOF", "Heredoc example", ""),
        ("VAR=$(echo 'hello' | tr 'a-z' 'A-Z')", "Command substitution", ""),
        ("npm install && npm test 2>&1 | tee test.log", "Complex build", ""),
    ]

    parser = BashParser()

    for cmd, desc, output in test_commands:
        result = parser.parse(cmd, desc, output)
        print(f"\n{'='*60}")
        print(f"Raw: {result.raw}")
        print(f"Category: {result.category.value}")
        print(f"Base commands: {result.base_commands}")
        print(f"Flags: {result.flags}")
        print(f"Pipes: {len(result.pipes)} segments")
        print(f"Redirects: {result.redirects}")
        print(f"Subshells: {result.subshells}")
        print(f"Variables: {result.variables}")
        print(f"Logical ops: {result.logical_ops}")
        print(f"Complexity: {result.complexity_score}")
        if result.parse_errors:
            print(f"Parse errors: {result.parse_errors}")
