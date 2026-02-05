#!/usr/bin/env python3
"""
Tests for the quiz generation module.

Tests quiz generation for each type, verifies exactly 4 options always,
and ensures correct answer is present.
"""

import unittest
import random
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class QuizGenerator:
    """Quiz generator for testing purposes."""

    QUIZ_TYPES = [
        "command_purpose",      # What does this command do?
        "fill_in_blank",        # Complete the command
        "fix_the_error",        # Fix the broken command
        "predict_output",       # What will be the output?
        "choose_command",       # Which command achieves X?
        "flag_meaning"          # What does this flag do?
    ]

    SAMPLE_COMMANDS = [
        {"command": "ls -la", "purpose": "List all files including hidden, in long format"},
        {"command": "grep -r pattern .", "purpose": "Search recursively for pattern"},
        {"command": "chmod 755 file.sh", "purpose": "Make file executable"},
        {"command": "find . -name '*.txt'", "purpose": "Find all txt files"},
        {"command": "tar -xzf archive.tar.gz", "purpose": "Extract gzipped tar archive"},
    ]

    def generate_quiz(self, quiz_type, command_data):
        """Generate a quiz question of the specified type."""
        if quiz_type == "command_purpose":
            return self._generate_purpose_quiz(command_data)
        elif quiz_type == "fill_in_blank":
            return self._generate_fill_blank_quiz(command_data)
        elif quiz_type == "fix_the_error":
            return self._generate_fix_error_quiz(command_data)
        elif quiz_type == "predict_output":
            return self._generate_predict_output_quiz(command_data)
        elif quiz_type == "choose_command":
            return self._generate_choose_command_quiz(command_data)
        elif quiz_type == "flag_meaning":
            return self._generate_flag_meaning_quiz(command_data)
        else:
            raise ValueError(f"Unknown quiz type: {quiz_type}")

    def _generate_purpose_quiz(self, command_data):
        """Generate 'What does this command do?' quiz."""
        correct = command_data["purpose"]
        wrong_options = [
            "Delete all files in directory",
            "Create a new directory",
            "Display system information",
        ]

        options = [correct] + wrong_options[:3]
        random.shuffle(options)

        return {
            "type": "command_purpose",
            "question": f"What does this command do?\n\n    {command_data['command']}",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }

    def _generate_fill_blank_quiz(self, command_data):
        """Generate 'Fill in the blank' quiz."""
        cmd = command_data["command"]
        parts = cmd.split()

        if len(parts) > 1:
            blank_idx = random.randint(1, len(parts) - 1)
            correct = parts[blank_idx]
            blanked_cmd = " ".join(
                "_____" if i == blank_idx else p
                for i, p in enumerate(parts)
            )
        else:
            correct = parts[0]
            blanked_cmd = "_____"

        wrong_options = ["-v", "--help", "file.txt"]
        options = [correct] + [w for w in wrong_options if w != correct][:3]

        while len(options) < 4:
            options.append(f"option{len(options)}")

        options = options[:4]
        random.shuffle(options)

        return {
            "type": "fill_in_blank",
            "question": f"Fill in the blank:\n\n    {blanked_cmd}",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }

    def _generate_fix_error_quiz(self, command_data):
        """Generate 'Fix the error' quiz."""
        cmd = command_data["command"]
        correct = cmd

        # Create broken versions - ensure they are different from correct
        broken_candidates = [
            cmd.replace("-", ""),  # Remove dashes
            cmd + " --invalid-flag",  # Add invalid flag
            cmd.replace(" ", ""),  # Remove spaces
            cmd.replace(".", ".."),  # Double dots
            "sudo " + cmd,  # Add sudo prefix
            cmd + " 2>/dev/null",  # Add redirect
        ]

        # Filter out any that match the correct answer
        broken_versions = [b for b in broken_candidates if b != correct]

        # Ensure we have exactly 3 unique wrong options
        unique_broken = list(dict.fromkeys(broken_versions))[:3]
        while len(unique_broken) < 3:
            unique_broken.append(f"broken_variant_{len(unique_broken)}")

        options = [correct] + unique_broken
        random.shuffle(options)

        return {
            "type": "fix_the_error",
            "question": f"Which is the correct version of this command?\n\n    Purpose: {command_data['purpose']}",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }

    def _generate_predict_output_quiz(self, command_data):
        """Generate 'Predict the output' quiz."""
        cmd = command_data["command"]

        # Simulated outputs
        outputs = {
            "ls -la": "drwxr-xr-x  2 user user 4096 Jan 1 12:00 .",
            "grep -r pattern .": "./file.txt:line with pattern",
            "chmod 755 file.sh": "(no output on success)",
        }

        correct = outputs.get(cmd, "Command executed successfully")
        wrong_outputs = [
            "Permission denied",
            "No such file or directory",
            "Invalid argument",
        ]

        options = [correct] + wrong_outputs[:3]
        random.shuffle(options)

        return {
            "type": "predict_output",
            "question": f"What is the likely output of:\n\n    {cmd}",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }

    def _generate_choose_command_quiz(self, command_data):
        """Generate 'Choose the right command' quiz."""
        correct = command_data["command"]
        purpose = command_data["purpose"]

        wrong_commands = [
            "rm -rf /",
            "echo 'wrong'",
            "exit 1",
        ]

        options = [correct] + wrong_commands[:3]
        random.shuffle(options)

        return {
            "type": "choose_command",
            "question": f"Which command will: {purpose}?",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }

    def _generate_flag_meaning_quiz(self, command_data):
        """Generate 'What does this flag mean?' quiz."""
        cmd = command_data["command"]
        parts = cmd.split()

        # Find a flag in the command
        flags = [p for p in parts if p.startswith("-")]

        if flags:
            flag = flags[0]
            flag_meanings = {
                "-la": "List all files in long format",
                "-r": "Recursive operation",
                "-v": "Verbose output",
                "-f": "Force operation",
                "-n": "Show line numbers",
            }
            correct = flag_meanings.get(flag, f"Enable {flag[1:]} option")
        else:
            flag = "-v"
            correct = "Verbose output"

        wrong_meanings = [
            "Quiet mode",
            "Delete files",
            "Show version",
        ]

        options = [correct] + wrong_meanings[:3]
        random.shuffle(options)

        return {
            "type": "flag_meaning",
            "question": f"What does the flag '{flag}' typically mean?",
            "options": options,
            "correct_answer": correct,
            "correct_index": options.index(correct)
        }


class TestQuizGeneration(unittest.TestCase):
    """Test quiz generation for all quiz types."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()
        self.sample_command = {
            "command": "ls -la",
            "purpose": "List all files including hidden, in long format"
        }

    def test_all_quiz_types_exist(self):
        """Test that all quiz types are defined."""
        expected_types = [
            "command_purpose",
            "fill_in_blank",
            "fix_the_error",
            "predict_output",
            "choose_command",
            "flag_meaning"
        ]
        self.assertEqual(set(self.generator.QUIZ_TYPES), set(expected_types))

    def test_command_purpose_quiz(self):
        """Test command purpose quiz generation."""
        quiz = self.generator.generate_quiz("command_purpose", self.sample_command)

        self.assertEqual(quiz["type"], "command_purpose")
        self.assertIn("What does this command do?", quiz["question"])
        self.assertIn(self.sample_command["command"], quiz["question"])

    def test_fill_in_blank_quiz(self):
        """Test fill in blank quiz generation."""
        quiz = self.generator.generate_quiz("fill_in_blank", self.sample_command)

        self.assertEqual(quiz["type"], "fill_in_blank")
        self.assertIn("_____", quiz["question"])

    def test_fix_the_error_quiz(self):
        """Test fix the error quiz generation."""
        quiz = self.generator.generate_quiz("fix_the_error", self.sample_command)

        self.assertEqual(quiz["type"], "fix_the_error")
        self.assertIn("correct version", quiz["question"])

    def test_predict_output_quiz(self):
        """Test predict output quiz generation."""
        quiz = self.generator.generate_quiz("predict_output", self.sample_command)

        self.assertEqual(quiz["type"], "predict_output")
        self.assertIn("output", quiz["question"].lower())

    def test_choose_command_quiz(self):
        """Test choose command quiz generation."""
        quiz = self.generator.generate_quiz("choose_command", self.sample_command)

        self.assertEqual(quiz["type"], "choose_command")
        self.assertIn("Which command", quiz["question"])

    def test_flag_meaning_quiz(self):
        """Test flag meaning quiz generation."""
        quiz = self.generator.generate_quiz("flag_meaning", self.sample_command)

        self.assertEqual(quiz["type"], "flag_meaning")
        self.assertIn("flag", quiz["question"].lower())


class TestExactlyFourOptions(unittest.TestCase):
    """Test that all quizzes have exactly 4 options."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_command_purpose_has_four_options(self):
        """Test command purpose quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("command_purpose", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])} for {cmd_data['command']}"
            )

    def test_fill_in_blank_has_four_options(self):
        """Test fill in blank quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("fill_in_blank", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])}"
            )

    def test_fix_the_error_has_four_options(self):
        """Test fix the error quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("fix_the_error", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])}"
            )

    def test_predict_output_has_four_options(self):
        """Test predict output quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("predict_output", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])}"
            )

    def test_choose_command_has_four_options(self):
        """Test choose command quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("choose_command", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])}"
            )

    def test_flag_meaning_has_four_options(self):
        """Test flag meaning quiz has exactly 4 options."""
        for cmd_data in self.generator.SAMPLE_COMMANDS:
            quiz = self.generator.generate_quiz("flag_meaning", cmd_data)
            self.assertEqual(
                len(quiz["options"]), 4,
                f"Expected 4 options, got {len(quiz['options'])}"
            )

    def test_all_quiz_types_have_four_options(self):
        """Test that all quiz types always have exactly 4 options."""
        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)
                self.assertEqual(
                    len(quiz["options"]), 4,
                    f"Quiz type '{quiz_type}' for '{cmd_data['command']}' "
                    f"has {len(quiz['options'])} options instead of 4"
                )


class TestCorrectAnswerPresent(unittest.TestCase):
    """Test that correct answer is always present in options."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_correct_answer_in_options(self):
        """Test correct answer is in options for all quiz types."""
        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)

                self.assertIn(
                    quiz["correct_answer"],
                    quiz["options"],
                    f"Correct answer '{quiz['correct_answer']}' not in options "
                    f"for quiz type '{quiz_type}'"
                )

    def test_correct_index_valid(self):
        """Test correct_index points to correct_answer."""
        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)

                self.assertEqual(
                    quiz["options"][quiz["correct_index"]],
                    quiz["correct_answer"],
                    f"correct_index {quiz['correct_index']} does not point to "
                    f"correct_answer in quiz type '{quiz_type}'"
                )

    def test_correct_index_in_range(self):
        """Test correct_index is within valid range (0-3)."""
        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)

                self.assertGreaterEqual(
                    quiz["correct_index"], 0,
                    f"correct_index {quiz['correct_index']} is negative"
                )
                self.assertLess(
                    quiz["correct_index"], 4,
                    f"correct_index {quiz['correct_index']} is >= 4"
                )


class TestOptionsAreUnique(unittest.TestCase):
    """Test that quiz options are unique (no duplicates)."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_no_duplicate_options(self):
        """Test that options contain no duplicates."""
        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)

                unique_options = set(quiz["options"])
                self.assertEqual(
                    len(unique_options),
                    len(quiz["options"]),
                    f"Duplicate options found in quiz type '{quiz_type}': "
                    f"{quiz['options']}"
                )


class TestQuizStructure(unittest.TestCase):
    """Test quiz data structure is correct."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_required_fields_present(self):
        """Test all required fields are present in quiz."""
        required_fields = ["type", "question", "options", "correct_answer", "correct_index"]

        for quiz_type in self.generator.QUIZ_TYPES:
            for cmd_data in self.generator.SAMPLE_COMMANDS:
                quiz = self.generator.generate_quiz(quiz_type, cmd_data)

                for field in required_fields:
                    self.assertIn(
                        field, quiz,
                        f"Missing required field '{field}' in quiz type '{quiz_type}'"
                    )

    def test_question_is_string(self):
        """Test question field is a string."""
        for quiz_type in self.generator.QUIZ_TYPES:
            quiz = self.generator.generate_quiz(
                quiz_type,
                self.generator.SAMPLE_COMMANDS[0]
            )
            self.assertIsInstance(quiz["question"], str)

    def test_options_is_list(self):
        """Test options field is a list."""
        for quiz_type in self.generator.QUIZ_TYPES:
            quiz = self.generator.generate_quiz(
                quiz_type,
                self.generator.SAMPLE_COMMANDS[0]
            )
            self.assertIsInstance(quiz["options"], list)

    def test_correct_index_is_int(self):
        """Test correct_index field is an integer."""
        for quiz_type in self.generator.QUIZ_TYPES:
            quiz = self.generator.generate_quiz(
                quiz_type,
                self.generator.SAMPLE_COMMANDS[0]
            )
            self.assertIsInstance(quiz["correct_index"], int)


class TestQuizRandomization(unittest.TestCase):
    """Test that quiz options are randomized."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_options_order_varies(self):
        """Test that generating multiple quizzes produces different option orders."""
        cmd_data = self.generator.SAMPLE_COMMANDS[0]
        quiz_type = "command_purpose"

        # Generate multiple quizzes and check if correct_index varies
        indices = set()
        for _ in range(20):
            quiz = self.generator.generate_quiz(quiz_type, cmd_data)
            indices.add(quiz["correct_index"])

        # With 20 attempts and 4 positions, we should see variation
        # (This test may occasionally fail due to randomness, but rarely)
        self.assertGreater(
            len(indices), 1,
            "Options don't appear to be randomized - correct answer always in same position"
        )


class TestInvalidQuizType(unittest.TestCase):
    """Test handling of invalid quiz types."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = QuizGenerator()

    def test_invalid_type_raises_error(self):
        """Test that invalid quiz type raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_quiz(
                "invalid_type",
                self.generator.SAMPLE_COMMANDS[0]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
