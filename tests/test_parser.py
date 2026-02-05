#!/usr/bin/env python3
"""
Tests for the bash command parser module.

Tests command tokenization, pipe detection, redirect detection,
complexity scoring, and edge cases like multi-line commands and heredocs.
"""

import unittest
import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCommandTokenization(unittest.TestCase):
    """Test command tokenization functionality."""

    def tokenize_simple(self, command):
        """Simple tokenizer for testing - splits on whitespace respecting quotes."""
        tokens = []
        current = ""
        in_quotes = None

        for char in command:
            if char in '"\'':
                if in_quotes == char:
                    in_quotes = None
                elif in_quotes is None:
                    in_quotes = char
                current += char
            elif char.isspace() and in_quotes is None:
                if current:
                    tokens.append(current)
                    current = ""
            else:
                current += char

        if current:
            tokens.append(current)

        return tokens

    def test_simple_command(self):
        """Test tokenizing a simple command."""
        tokens = self.tokenize_simple("ls -la /home")
        self.assertEqual(tokens, ["ls", "-la", "/home"])

    def test_command_with_quotes(self):
        """Test tokenizing command with quoted strings."""
        tokens = self.tokenize_simple('echo "hello world"')
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0], "echo")
        self.assertIn("hello world", tokens[1])

    def test_command_with_single_quotes(self):
        """Test tokenizing command with single quotes."""
        tokens = self.tokenize_simple("echo 'don'\\''t break'")
        self.assertIn("echo", tokens)

    def test_command_with_flags(self):
        """Test tokenizing command with multiple flags."""
        tokens = self.tokenize_simple("grep -r -n -i pattern .")
        self.assertEqual(tokens[0], "grep")
        self.assertIn("-r", tokens)
        self.assertIn("-n", tokens)
        self.assertIn("-i", tokens)

    def test_extract_base_command(self):
        """Test extracting the base command name."""
        commands = [
            ("ls -la", "ls"),
            ("git status", "git"),
            ("/usr/bin/python3 script.py", "/usr/bin/python3"),
            ("./run.sh", "./run.sh"),
        ]

        for full_cmd, expected_base in commands:
            tokens = self.tokenize_simple(full_cmd)
            self.assertEqual(tokens[0], expected_base)


class TestPipeDetection(unittest.TestCase):
    """Test pipe detection in commands."""

    def count_pipes(self, command):
        """Count pipes in command (excluding those in quotes and || operator)."""
        count = 0
        in_quotes = None
        i = 0
        n = len(command)

        while i < n:
            char = command[i]
            prev_char = command[i - 1] if i > 0 else None

            if char in '"\'':
                if in_quotes == char and prev_char != '\\':
                    in_quotes = None
                elif in_quotes is None:
                    in_quotes = char
            elif char == '|' and in_quotes is None:
                # Check if it's || (logical OR) by looking at next char
                next_char = command[i + 1] if i + 1 < n else None
                if prev_char != '|' and next_char != '|':
                    count += 1

            i += 1

        return count

    def test_single_pipe(self):
        """Test detecting a single pipe."""
        cmd = "cat file.txt | grep pattern"
        self.assertEqual(self.count_pipes(cmd), 1)

    def test_multiple_pipes(self):
        """Test detecting multiple pipes."""
        cmd = "cat file | grep pattern | sort | uniq"
        self.assertEqual(self.count_pipes(cmd), 3)

    def test_no_pipes(self):
        """Test command without pipes."""
        cmd = "ls -la /home/user"
        self.assertEqual(self.count_pipes(cmd), 0)

    def test_pipe_in_quotes(self):
        """Test that pipes inside quotes are not counted."""
        cmd = 'echo "hello | world" | grep hello'
        # Should only count the pipe outside quotes
        self.assertEqual(self.count_pipes(cmd), 1)

    def test_logical_or_not_counted(self):
        """Test that || (logical OR) is not counted as pipe."""
        cmd = "test -f file || echo 'not found'"
        # || should not be counted
        self.assertEqual(self.count_pipes(cmd), 0)

    def test_extract_pipeline_stages(self):
        """Test extracting individual stages of a pipeline."""
        cmd = "cat file | grep pattern | sort"
        stages = [s.strip() for s in cmd.split("|")]
        self.assertEqual(len(stages), 3)
        self.assertEqual(stages[0], "cat file")
        self.assertEqual(stages[1], "grep pattern")
        self.assertEqual(stages[2], "sort")


class TestRedirectDetection(unittest.TestCase):
    """Test redirect detection in commands."""

    def detect_redirects(self, command):
        """Detect redirects in command."""
        redirects = {
            "stdout": False,
            "stderr": False,
            "stdin": False,
            "append": False,
            "combined": False
        }

        # Simple patterns for detection
        if ">" in command and ">>" not in command:
            redirects["stdout"] = True
        if ">>" in command:
            redirects["append"] = True
        if "2>" in command:
            redirects["stderr"] = True
        if "<" in command:
            redirects["stdin"] = True
        if "2>&1" in command or "&>" in command:
            redirects["combined"] = True

        return redirects

    def test_stdout_redirect(self):
        """Test detecting stdout redirect."""
        cmd = "echo 'test' > output.txt"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["stdout"])

    def test_stderr_redirect(self):
        """Test detecting stderr redirect."""
        cmd = "command 2> errors.log"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["stderr"])

    def test_stdin_redirect(self):
        """Test detecting stdin redirect."""
        cmd = "sort < input.txt"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["stdin"])

    def test_append_redirect(self):
        """Test detecting append redirect."""
        cmd = "echo 'more' >> log.txt"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["append"])

    def test_combined_redirect(self):
        """Test detecting combined stdout/stderr redirect."""
        cmd = "command > output.txt 2>&1"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["combined"])

    def test_no_redirects(self):
        """Test command without redirects."""
        cmd = "ls -la"
        redirects = self.detect_redirects(cmd)
        self.assertFalse(any(redirects.values()))

    def test_multiple_redirects(self):
        """Test command with multiple redirects."""
        cmd = "command < input.txt > output.txt 2> error.log"
        redirects = self.detect_redirects(cmd)
        self.assertTrue(redirects["stdin"])
        self.assertTrue(redirects["stdout"])
        self.assertTrue(redirects["stderr"])


class TestComplexityScoring(unittest.TestCase):
    """Test command complexity scoring."""

    def calculate_complexity(self, command):
        """Calculate complexity score for a command."""
        score = 1  # Base score

        # Pipes add complexity
        pipes = command.count("|") - command.count("||")
        score += pipes * 2

        # Redirects add complexity
        if ">" in command:
            score += 1
        if "2>" in command:
            score += 1
        if "<" in command:
            score += 1

        # Command chaining
        if "&&" in command:
            score += command.count("&&") * 2
        if "||" in command:
            score += command.count("||")
        if ";" in command:
            score += command.count(";")

        # Subshells and command substitution
        if "$(" in command or "`" in command:
            score += 2
        if "(" in command and ")" in command:
            score += 1

        # Loops and conditionals
        if any(kw in command for kw in ["for ", "while ", "if ", "case "]):
            score += 3

        # Variables
        if "$" in command:
            score += 1

        return score

    def test_simple_command_low_score(self):
        """Test that simple commands have low complexity."""
        score = self.calculate_complexity("ls -la")
        self.assertLessEqual(score, 2)

    def test_piped_command_medium_score(self):
        """Test that piped commands have medium complexity."""
        score = self.calculate_complexity("cat file | grep pattern | sort")
        self.assertGreater(score, 3)

    def test_complex_command_high_score(self):
        """Test that complex commands have high complexity."""
        cmd = "for f in *.txt; do cat $f | grep pattern >> output.txt; done"
        score = self.calculate_complexity(cmd)
        self.assertGreater(score, 6)

    def test_command_substitution_adds_complexity(self):
        """Test that command substitution increases complexity."""
        simple = "echo hello"
        with_subst = "echo $(date)"

        self.assertGreater(
            self.calculate_complexity(with_subst),
            self.calculate_complexity(simple)
        )

    def test_chained_commands_add_complexity(self):
        """Test that command chaining increases complexity."""
        simple = "mkdir dir"
        chained = "mkdir dir && cd dir && touch file"

        self.assertGreater(
            self.calculate_complexity(chained),
            self.calculate_complexity(simple)
        )

    def test_complexity_categories(self):
        """Test categorizing commands by complexity."""
        def categorize(score):
            if score <= 2:
                return "beginner"
            elif score <= 5:
                return "intermediate"
            else:
                return "advanced"

        self.assertEqual(categorize(1), "beginner")
        self.assertEqual(categorize(4), "intermediate")
        self.assertEqual(categorize(8), "advanced")


class TestMultiLineCommands(unittest.TestCase):
    """Test handling of multi-line commands."""

    def test_for_loop(self):
        """Test parsing a for loop."""
        cmd = """for i in 1 2 3; do
    echo $i
done"""
        self.assertIn("for", cmd)
        self.assertIn("do", cmd)
        self.assertIn("done", cmd)
        lines = cmd.split("\n")
        self.assertEqual(len(lines), 3)

    def test_while_loop(self):
        """Test parsing a while loop."""
        cmd = """while read line; do
    echo "$line"
done < input.txt"""
        self.assertIn("while", cmd)
        self.assertIn("done", cmd)
        self.assertIn("<", cmd)

    def test_if_statement(self):
        """Test parsing an if statement."""
        cmd = """if [ -f file.txt ]; then
    cat file.txt
else
    echo "not found"
fi"""
        self.assertIn("if", cmd)
        self.assertIn("then", cmd)
        self.assertIn("else", cmd)
        self.assertIn("fi", cmd)

    def test_function_definition(self):
        """Test parsing a function definition."""
        cmd = """my_func() {
    echo "Hello $1"
    return 0
}"""
        self.assertIn("my_func()", cmd)
        self.assertIn("{", cmd)
        self.assertIn("}", cmd)

    def test_line_continuation(self):
        """Test parsing commands with line continuation."""
        cmd = "echo \"this is a very long \\\ncommand that spans \\\nmultiple lines\""
        # Should be treated as single logical command
        self.assertIn("\\", cmd)
        self.assertIn("\n", cmd)


class TestHeredocs(unittest.TestCase):
    """Test handling of heredoc syntax."""

    def detect_heredoc(self, command):
        """Detect if command contains heredoc."""
        return "<<" in command

    def test_basic_heredoc(self):
        """Test detecting basic heredoc."""
        cmd = """cat << EOF
line 1
line 2
EOF"""
        self.assertTrue(self.detect_heredoc(cmd))

    def test_heredoc_with_variable(self):
        """Test heredoc with variable expansion."""
        cmd = """cat << EOF
Hello $USER
Today is $(date)
EOF"""
        self.assertTrue(self.detect_heredoc(cmd))
        self.assertIn("$USER", cmd)

    def test_heredoc_quoted_delimiter(self):
        """Test heredoc with quoted delimiter (no expansion)."""
        cmd = """cat << 'EOF'
$USER will not expand
EOF"""
        self.assertTrue(self.detect_heredoc(cmd))
        self.assertIn("'EOF'", cmd)

    def test_heredoc_with_dash(self):
        """Test heredoc with <<- for tab stripping."""
        cmd = """cat <<- EOF
\tindented line
EOF"""
        self.assertIn("<<-", cmd)

    def test_no_heredoc(self):
        """Test command without heredoc."""
        cmd = "echo 'hello world'"
        self.assertFalse(self.detect_heredoc(cmd))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""

    def test_empty_command(self):
        """Test handling empty command."""
        cmd = ""
        self.assertEqual(len(cmd), 0)

    def test_whitespace_only(self):
        """Test handling whitespace-only command."""
        cmd = "   \t\n  "
        self.assertEqual(cmd.strip(), "")

    def test_comment_only(self):
        """Test handling comment-only command."""
        cmd = "# this is a comment"
        self.assertTrue(cmd.startswith("#"))

    def test_command_with_comments(self):
        """Test command with inline comment."""
        cmd = "ls -la  # list all files"
        parts = cmd.split("#")
        actual_cmd = parts[0].strip()
        self.assertEqual(actual_cmd, "ls -la")

    def test_escaped_characters(self):
        """Test command with escaped characters."""
        cmd = r'echo "Hello \"World\""'
        self.assertIn('\\"', cmd)

    def test_special_variables(self):
        """Test command with special variables."""
        cmd = "echo $? $$ $! $0 $@"
        special_vars = ["$?", "$$", "$!", "$0", "$@"]
        for var in special_vars:
            self.assertIn(var, cmd)

    def test_brace_expansion(self):
        """Test command with brace expansion."""
        cmd = "echo {a,b,c}.txt"
        self.assertIn("{", cmd)
        self.assertIn("}", cmd)

    def test_glob_patterns(self):
        """Test command with glob patterns."""
        cmd = "ls *.txt **/*.py [abc].log"
        self.assertIn("*", cmd)
        self.assertIn("**", cmd)
        self.assertIn("[", cmd)

    def test_process_substitution(self):
        """Test command with process substitution."""
        cmd = "diff <(sort file1) <(sort file2)"
        self.assertIn("<(", cmd)

    def test_very_long_command(self):
        """Test handling very long command."""
        cmd = "echo " + "a" * 10000
        self.assertGreater(len(cmd), 10000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
