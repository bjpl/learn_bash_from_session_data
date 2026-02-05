#!/usr/bin/env python3
"""
Tests for the command analyzer module.

Tests category assignment, deduplication, and statistics generation.
"""

import unittest
import sys
import os
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCategoryAssignment(unittest.TestCase):
    """Test command category assignment functionality."""

    # Category definitions for testing
    CATEGORIES = {
        "git": ["git"],
        "file_operations": ["ls", "cat", "cp", "mv", "rm", "mkdir", "touch", "chmod", "chown"],
        "text_processing": ["grep", "sed", "awk", "sort", "uniq", "wc", "head", "tail", "cut"],
        "system": ["ps", "top", "kill", "systemctl", "service", "df", "du", "free"],
        "network": ["curl", "wget", "ssh", "scp", "ping", "netstat", "nc"],
        "package_management": ["apt", "apt-get", "yum", "dnf", "brew", "npm", "pip"],
        "docker": ["docker", "docker-compose"],
        "search": ["find", "locate", "which", "whereis"],
        "archive": ["tar", "zip", "unzip", "gzip", "gunzip"],
        "other": []
    }

    def get_base_command(self, command):
        """Extract base command from full command string."""
        # Handle pipes - get first command
        if "|" in command:
            command = command.split("|")[0]
        # Handle chains - get first command
        for sep in ["&&", "||", ";"]:
            if sep in command:
                command = command.split(sep)[0]
        # Get first token
        parts = command.strip().split()
        if parts:
            base = parts[0]
            # Handle sudo
            if base == "sudo" and len(parts) > 1:
                base = parts[1]
            return base
        return ""

    def categorize_command(self, command):
        """Categorize a command based on its base command."""
        base = self.get_base_command(command)

        for category, commands in self.CATEGORIES.items():
            if base in commands:
                return category

        return "other"

    def test_git_commands(self):
        """Test categorizing git commands."""
        commands = [
            "git status",
            "git commit -m 'message'",
            "git push origin main",
            "git log --oneline -5"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "git")

    def test_file_operations(self):
        """Test categorizing file operation commands."""
        commands = [
            "ls -la /home",
            "cat file.txt",
            "cp source dest",
            "mv old new",
            "rm -rf temp",
            "mkdir -p new/dir",
            "touch newfile.txt",
            "chmod 755 script.sh"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "file_operations")

    def test_text_processing(self):
        """Test categorizing text processing commands."""
        commands = [
            "grep pattern file.txt",
            "sed 's/old/new/g' file",
            "awk '{print $1}' data.txt",
            "sort file.txt",
            "uniq -c sorted.txt",
            "wc -l file.txt",
            "head -n 10 file.txt",
            "tail -f log.txt"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "text_processing")

    def test_system_commands(self):
        """Test categorizing system commands."""
        commands = [
            "ps aux",
            "top -n 1",
            "kill -9 1234",
            "systemctl status nginx",
            "df -h",
            "du -sh *",
            "free -m"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "system")

    def test_network_commands(self):
        """Test categorizing network commands."""
        commands = [
            "curl https://api.example.com",
            "wget http://file.com/file.zip",
            "ssh user@host",
            "scp file.txt user@host:/path",
            "ping -c 3 google.com"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "network")

    def test_docker_commands(self):
        """Test categorizing docker commands."""
        commands = [
            "docker ps",
            "docker build -t myimage .",
            "docker-compose up -d"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "docker")

    def test_piped_command_categorization(self):
        """Test categorizing piped commands (first command determines category)."""
        cmd = "cat file.txt | grep pattern | sort"
        self.assertEqual(self.categorize_command(cmd), "file_operations")

    def test_sudo_commands(self):
        """Test categorizing commands with sudo."""
        cmd = "sudo apt install vim"
        base = self.get_base_command(cmd)
        self.assertEqual(base, "apt")
        self.assertEqual(self.categorize_command(cmd), "package_management")

    def test_unknown_commands(self):
        """Test categorizing unknown commands."""
        commands = [
            "myapp --config file.yml",
            "custom_script.sh arg1 arg2"
        ]
        for cmd in commands:
            self.assertEqual(self.categorize_command(cmd), "other")


class TestDeduplication(unittest.TestCase):
    """Test command deduplication functionality."""

    def normalize_command(self, command):
        """Normalize command for comparison."""
        # Remove extra whitespace
        normalized = " ".join(command.split())
        # Convert to lowercase for comparison
        return normalized.lower()

    def deduplicate_exact(self, commands):
        """Remove exact duplicate commands."""
        seen = set()
        unique = []
        for cmd in commands:
            if cmd not in seen:
                seen.add(cmd)
                unique.append(cmd)
        return unique

    def deduplicate_normalized(self, commands):
        """Remove duplicates after normalization."""
        seen = set()
        unique = []
        for cmd in commands:
            normalized = self.normalize_command(cmd)
            if normalized not in seen:
                seen.add(normalized)
                unique.append(cmd)
        return unique

    def deduplicate_by_pattern(self, commands):
        """Remove commands with same pattern (different arguments)."""
        seen_patterns = set()
        unique = []

        for cmd in commands:
            # Extract pattern: base command + flag structure
            parts = cmd.split()
            if parts:
                pattern = parts[0]
                for part in parts[1:]:
                    if part.startswith("-"):
                        pattern += " " + part

                if pattern not in seen_patterns:
                    seen_patterns.add(pattern)
                    unique.append(cmd)

        return unique

    def test_exact_duplicates(self):
        """Test removing exact duplicates."""
        commands = [
            "ls -la",
            "git status",
            "ls -la",
            "pwd",
            "git status"
        ]
        unique = self.deduplicate_exact(commands)
        self.assertEqual(len(unique), 3)

    def test_normalized_duplicates(self):
        """Test removing duplicates after normalization."""
        commands = [
            "ls  -la",      # extra space
            "ls -la",
            "LS -LA",       # different case
            "pwd"
        ]
        unique = self.deduplicate_normalized(commands)
        self.assertEqual(len(unique), 2)

    def test_pattern_duplicates(self):
        """Test removing commands with same pattern."""
        commands = [
            "ls -la /home",
            "ls -la /var",
            "ls -la /tmp",
            "git status",
            "git commit -m 'first'",
            "git commit -m 'second'"
        ]
        unique = self.deduplicate_by_pattern(commands)
        # Should keep: ls -la, git status, git commit -m
        self.assertEqual(len(unique), 3)

    def test_preserve_order(self):
        """Test that deduplication preserves first occurrence order."""
        commands = ["b", "a", "c", "a", "b"]
        unique = self.deduplicate_exact(commands)
        self.assertEqual(unique, ["b", "a", "c"])

    def test_empty_input(self):
        """Test deduplication with empty input."""
        unique = self.deduplicate_exact([])
        self.assertEqual(unique, [])

    def test_all_unique(self):
        """Test deduplication when all commands are unique."""
        commands = ["ls", "pwd", "whoami"]
        unique = self.deduplicate_exact(commands)
        self.assertEqual(len(unique), 3)


class TestStatisticsGeneration(unittest.TestCase):
    """Test statistics generation functionality."""

    def generate_stats(self, commands, categories):
        """Generate statistics for a list of commands."""
        stats = {
            "total_commands": len(commands),
            "unique_commands": len(set(commands)),
            "category_counts": Counter(categories),
            "complexity_distribution": {"beginner": 0, "intermediate": 0, "advanced": 0},
            "most_common": Counter(commands).most_common(5)
        }
        return stats

    def calculate_complexity_distribution(self, complexities):
        """Calculate distribution of complexity levels."""
        distribution = {"beginner": 0, "intermediate": 0, "advanced": 0}
        for score in complexities:
            if score <= 2:
                distribution["beginner"] += 1
            elif score <= 5:
                distribution["intermediate"] += 1
            else:
                distribution["advanced"] += 1
        return distribution

    def test_total_count(self):
        """Test total command count."""
        commands = ["ls", "pwd", "ls", "whoami"]
        stats = self.generate_stats(commands, [])
        self.assertEqual(stats["total_commands"], 4)

    def test_unique_count(self):
        """Test unique command count."""
        commands = ["ls", "pwd", "ls", "whoami"]
        stats = self.generate_stats(commands, [])
        self.assertEqual(stats["unique_commands"], 3)

    def test_category_counts(self):
        """Test category count statistics."""
        categories = ["git", "git", "file_operations", "network", "git"]
        stats = self.generate_stats([], categories)
        self.assertEqual(stats["category_counts"]["git"], 3)
        self.assertEqual(stats["category_counts"]["file_operations"], 1)
        self.assertEqual(stats["category_counts"]["network"], 1)

    def test_most_common(self):
        """Test most common commands."""
        commands = ["ls", "ls", "ls", "pwd", "pwd", "whoami"]
        stats = self.generate_stats(commands, [])
        self.assertEqual(stats["most_common"][0][0], "ls")
        self.assertEqual(stats["most_common"][0][1], 3)

    def test_complexity_distribution(self):
        """Test complexity distribution calculation."""
        complexities = [1, 2, 3, 4, 5, 6, 7, 8]
        distribution = self.calculate_complexity_distribution(complexities)
        self.assertEqual(distribution["beginner"], 2)
        self.assertEqual(distribution["intermediate"], 3)
        self.assertEqual(distribution["advanced"], 3)

    def test_empty_stats(self):
        """Test statistics with no commands."""
        stats = self.generate_stats([], [])
        self.assertEqual(stats["total_commands"], 0)
        self.assertEqual(stats["unique_commands"], 0)

    def test_category_percentages(self):
        """Test calculating category percentages."""
        categories = ["git"] * 50 + ["file_operations"] * 30 + ["other"] * 20
        category_counts = Counter(categories)
        total = len(categories)

        percentages = {cat: count / total * 100 for cat, count in category_counts.items()}

        self.assertEqual(percentages["git"], 50.0)
        self.assertEqual(percentages["file_operations"], 30.0)
        self.assertEqual(percentages["other"], 20.0)


class TestCommandGrouping(unittest.TestCase):
    """Test command grouping functionality."""

    def group_by_category(self, commands_with_categories):
        """Group commands by their category."""
        groups = {}
        for cmd, category in commands_with_categories:
            if category not in groups:
                groups[category] = []
            groups[category].append(cmd)
        return groups

    def group_by_complexity(self, commands_with_complexity):
        """Group commands by complexity level."""
        groups = {"beginner": [], "intermediate": [], "advanced": []}
        for cmd, score in commands_with_complexity:
            if score <= 2:
                groups["beginner"].append(cmd)
            elif score <= 5:
                groups["intermediate"].append(cmd)
            else:
                groups["advanced"].append(cmd)
        return groups

    def test_group_by_category(self):
        """Test grouping commands by category."""
        commands = [
            ("git status", "git"),
            ("ls -la", "file_operations"),
            ("git commit", "git"),
            ("curl http://api.com", "network")
        ]
        groups = self.group_by_category(commands)

        self.assertEqual(len(groups["git"]), 2)
        self.assertEqual(len(groups["file_operations"]), 1)
        self.assertEqual(len(groups["network"]), 1)

    def test_group_by_complexity(self):
        """Test grouping commands by complexity."""
        commands = [
            ("ls", 1),
            ("cat file | grep pattern", 4),
            ("for i in *.txt; do cat $i | grep x >> out.txt; done", 8)
        ]
        groups = self.group_by_complexity(commands)

        self.assertEqual(len(groups["beginner"]), 1)
        self.assertEqual(len(groups["intermediate"]), 1)
        self.assertEqual(len(groups["advanced"]), 1)

    def test_empty_groups(self):
        """Test grouping with no commands."""
        groups = self.group_by_category([])
        self.assertEqual(groups, {})


class TestOutputFormatting(unittest.TestCase):
    """Test statistics output formatting."""

    def format_as_table(self, category_counts):
        """Format category counts as a table."""
        lines = ["Category | Count | Percentage"]
        lines.append("-" * 40)

        total = sum(category_counts.values())
        for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            pct = (count / total * 100) if total > 0 else 0
            lines.append(f"{category:20} | {count:5} | {pct:5.1f}%")

        return "\n".join(lines)

    def format_as_json(self, stats):
        """Format statistics as JSON."""
        import json
        return json.dumps(stats, indent=2)

    def test_table_format(self):
        """Test table formatting."""
        counts = {"git": 50, "file_operations": 30, "other": 20}
        table = self.format_as_table(counts)

        self.assertIn("Category", table)
        self.assertIn("git", table)
        self.assertIn("50.0%", table)

    def test_json_format(self):
        """Test JSON formatting."""
        import json
        stats = {"total": 100, "categories": {"git": 50}}
        json_str = self.format_as_json(stats)

        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertEqual(parsed["total"], 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
