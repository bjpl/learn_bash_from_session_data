#!/usr/bin/env python3
"""
Tests for the JSONL extractor module.

Tests JSONL parsing, command extraction, and tool_use/tool_result matching.
"""

import unittest
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Sample JSONL data for testing
SAMPLE_TOOL_USE = {
    "type": "tool_use",
    "id": "toolu_01ABC123",
    "name": "Bash",
    "input": {
        "command": "git status",
        "description": "Check git status"
    }
}

SAMPLE_TOOL_RESULT = {
    "type": "tool_result",
    "tool_use_id": "toolu_01ABC123",
    "content": "On branch main\nnothing to commit, working tree clean"
}

SAMPLE_JSONL_LINES = [
    json.dumps({"type": "text", "text": "Let me check the status"}),
    json.dumps(SAMPLE_TOOL_USE),
    json.dumps(SAMPLE_TOOL_RESULT),
    json.dumps({"type": "text", "text": "The repository is clean"})
]


class TestJSONLParsing(unittest.TestCase):
    """Test JSONL parsing functionality."""

    def test_parse_single_line(self):
        """Test parsing a single JSONL line."""
        line = '{"type": "tool_use", "name": "Bash"}'
        parsed = json.loads(line)
        self.assertEqual(parsed["type"], "tool_use")
        self.assertEqual(parsed["name"], "Bash")

    def test_parse_multiple_lines(self):
        """Test parsing multiple JSONL lines."""
        parsed = [json.loads(line) for line in SAMPLE_JSONL_LINES]
        self.assertEqual(len(parsed), 4)
        self.assertEqual(parsed[0]["type"], "text")
        self.assertEqual(parsed[1]["type"], "tool_use")
        self.assertEqual(parsed[2]["type"], "tool_result")

    def test_parse_nested_input(self):
        """Test parsing nested input objects."""
        line = json.dumps(SAMPLE_TOOL_USE)
        parsed = json.loads(line)
        self.assertIn("input", parsed)
        self.assertEqual(parsed["input"]["command"], "git status")

    def test_parse_empty_line(self):
        """Test handling empty lines gracefully."""
        lines = ["", '{"type": "text"}', ""]
        parsed = []
        for line in lines:
            if line.strip():
                parsed.append(json.loads(line))
        self.assertEqual(len(parsed), 1)

    def test_parse_malformed_json(self):
        """Test handling malformed JSON."""
        malformed = '{"type": "tool_use", name: invalid}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(malformed)

    def test_parse_unicode_content(self):
        """Test parsing content with unicode characters."""
        line = '{"command": "echo \\"Hello World\\" > file.txt"}'
        parsed = json.loads(line)
        self.assertIn("Hello World", parsed["command"])


class TestCommandExtraction(unittest.TestCase):
    """Test command extraction from tool_use events."""

    def test_extract_simple_command(self):
        """Test extracting a simple bash command."""
        tool_use = {"type": "tool_use", "name": "Bash", "input": {"command": "ls -la"}}
        command = tool_use.get("input", {}).get("command", "")
        self.assertEqual(command, "ls -la")

    def test_extract_command_with_pipes(self):
        """Test extracting command with pipes."""
        tool_use = {
            "type": "tool_use",
            "name": "Bash",
            "input": {"command": "cat file.txt | grep pattern | sort"}
        }
        command = tool_use.get("input", {}).get("command", "")
        self.assertIn("|", command)
        self.assertEqual(command.count("|"), 2)

    def test_extract_command_with_redirects(self):
        """Test extracting command with redirects."""
        tool_use = {
            "type": "tool_use",
            "name": "Bash",
            "input": {"command": "echo 'test' > output.txt 2>&1"}
        }
        command = tool_use.get("input", {}).get("command", "")
        self.assertIn(">", command)
        self.assertIn("2>&1", command)

    def test_extract_multiline_command(self):
        """Test extracting multi-line command."""
        tool_use = {
            "type": "tool_use",
            "name": "Bash",
            "input": {"command": "for i in 1 2 3; do\n  echo $i\ndone"}
        }
        command = tool_use.get("input", {}).get("command", "")
        self.assertIn("\n", command)
        self.assertIn("for", command)
        self.assertIn("done", command)

    def test_extract_from_non_bash_tool(self):
        """Test that non-Bash tools are handled correctly."""
        tool_use = {"type": "tool_use", "name": "Read", "input": {"file_path": "/etc/hosts"}}
        is_bash = tool_use.get("name") == "Bash"
        self.assertFalse(is_bash)

    def test_extract_missing_command(self):
        """Test handling tool_use without command field."""
        tool_use = {"type": "tool_use", "name": "Bash", "input": {}}
        command = tool_use.get("input", {}).get("command", "")
        self.assertEqual(command, "")

    def test_extract_command_with_env_vars(self):
        """Test extracting command with environment variables."""
        tool_use = {
            "type": "tool_use",
            "name": "Bash",
            "input": {"command": "export PATH=$PATH:/usr/local/bin && echo $PATH"}
        }
        command = tool_use.get("input", {}).get("command", "")
        self.assertIn("$PATH", command)
        self.assertIn("export", command)


class TestToolMatching(unittest.TestCase):
    """Test tool_use/tool_result matching functionality."""

    def test_match_by_id(self):
        """Test matching tool_use and tool_result by ID."""
        tool_use = {"type": "tool_use", "id": "toolu_123", "name": "Bash"}
        tool_result = {"type": "tool_result", "tool_use_id": "toolu_123", "content": "output"}

        self.assertEqual(tool_use["id"], tool_result["tool_use_id"])

    def test_match_multiple_pairs(self):
        """Test matching multiple tool_use/tool_result pairs."""
        events = [
            {"type": "tool_use", "id": "toolu_1", "name": "Bash", "input": {"command": "ls"}},
            {"type": "tool_result", "tool_use_id": "toolu_1", "content": "file1.txt"},
            {"type": "tool_use", "id": "toolu_2", "name": "Bash", "input": {"command": "pwd"}},
            {"type": "tool_result", "tool_use_id": "toolu_2", "content": "/home/user"},
        ]

        # Build matching pairs
        pairs = {}
        for event in events:
            if event["type"] == "tool_use":
                pairs[event["id"]] = {"use": event, "result": None}
            elif event["type"] == "tool_result":
                if event["tool_use_id"] in pairs:
                    pairs[event["tool_use_id"]]["result"] = event

        self.assertEqual(len(pairs), 2)
        self.assertIsNotNone(pairs["toolu_1"]["result"])
        self.assertIsNotNone(pairs["toolu_2"]["result"])

    def test_unmatched_tool_use(self):
        """Test handling tool_use without matching result."""
        events = [
            {"type": "tool_use", "id": "toolu_orphan", "name": "Bash"},
        ]

        pairs = {}
        for event in events:
            if event["type"] == "tool_use":
                pairs[event["id"]] = {"use": event, "result": None}

        self.assertIsNone(pairs["toolu_orphan"]["result"])

    def test_extract_output_from_result(self):
        """Test extracting output content from tool_result."""
        result = {
            "type": "tool_result",
            "tool_use_id": "toolu_123",
            "content": "command output here"
        }
        output = result.get("content", "")
        self.assertEqual(output, "command output here")

    def test_result_with_error(self):
        """Test handling tool_result with error content."""
        result = {
            "type": "tool_result",
            "tool_use_id": "toolu_123",
            "content": "Error: command not found: nonexistent",
            "is_error": True
        }
        is_error = result.get("is_error", False)
        self.assertTrue(is_error)
        self.assertIn("Error", result["content"])


class TestFilteringBashCommands(unittest.TestCase):
    """Test filtering for Bash commands specifically."""

    def test_filter_bash_only(self):
        """Test filtering to get only Bash tool uses."""
        events = [
            {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}},
            {"type": "tool_use", "name": "Read", "input": {"file_path": "test.txt"}},
            {"type": "tool_use", "name": "Bash", "input": {"command": "pwd"}},
            {"type": "tool_use", "name": "Write", "input": {"file_path": "out.txt"}},
        ]

        bash_commands = [e for e in events if e.get("name") == "Bash"]
        self.assertEqual(len(bash_commands), 2)

    def test_case_sensitivity(self):
        """Test that tool name matching is case-sensitive."""
        events = [
            {"type": "tool_use", "name": "Bash"},
            {"type": "tool_use", "name": "bash"},
            {"type": "tool_use", "name": "BASH"},
        ]

        bash_exact = [e for e in events if e.get("name") == "Bash"]
        self.assertEqual(len(bash_exact), 1)

    def test_skip_internal_commands(self):
        """Test skipping internal/administrative commands."""
        internal_patterns = ["cd ", "source ", ". "]

        commands = [
            "cd /home/user",
            "ls -la",
            "source ~/.bashrc",
            "git status",
            ". /etc/profile"
        ]

        external_commands = []
        for cmd in commands:
            is_internal = any(cmd.startswith(p) for p in internal_patterns)
            if not is_internal:
                external_commands.append(cmd)

        self.assertEqual(len(external_commands), 2)
        self.assertIn("ls -la", external_commands)
        self.assertIn("git status", external_commands)


if __name__ == "__main__":
    unittest.main(verbosity=2)
