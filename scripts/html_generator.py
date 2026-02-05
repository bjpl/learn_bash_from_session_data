#!/usr/bin/env python3
"""
HTML Generator for Bash Learning Report

Generates a single self-contained HTML file with all CSS and JS inline.
No external dependencies - pure Python standard library.
"""

from typing import Any, List
from datetime import datetime
from pathlib import Path
import html
import json


def _generate_html_impl(analysis_result: dict[str, Any], quizzes: list[dict[str, Any]]) -> str:
    """
    Generate complete HTML report from analysis results and quizzes.

    Args:
        analysis_result: Dictionary containing parsed commands, stats, categories
        quizzes: List of quiz question dictionaries

    Returns:
        Complete HTML string ready to write to file
    """
    stats = analysis_result.get("stats", {})
    commands = analysis_result.get("commands", [])
    categories = analysis_result.get("categories", {})

    overview_html = render_overview_tab(stats, commands, categories)
    commands_html = render_commands_tab(commands)
    lessons_html = render_lessons_tab(categories, commands)
    quiz_html = render_quiz_tab(quizzes)

    inline_css = get_inline_css()
    inline_js = get_inline_js(quizzes)

    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bash Command Learning Report</title>
    <style>
{inline_css}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1>Bash Command Learning Report</h1>
                <p class="subtitle">Generated: {generation_time}</p>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
                <span class="theme-icon light-icon">&#9728;</span>
                <span class="theme-icon dark-icon">&#9790;</span>
            </button>
        </header>

        <nav class="tabs" role="tablist">
            <button class="tab active" data-tab="overview" role="tab" aria-selected="true" aria-controls="panel-overview">
                <span class="tab-icon">&#9776;</span>
                <span class="tab-label">Overview</span>
                <span class="tab-key">1</span>
            </button>
            <button class="tab" data-tab="commands" role="tab" aria-selected="false" aria-controls="panel-commands">
                <span class="tab-icon">&#10095;</span>
                <span class="tab-label">Commands</span>
                <span class="tab-key">2</span>
            </button>
            <button class="tab" data-tab="lessons" role="tab" aria-selected="false" aria-controls="panel-lessons">
                <span class="tab-icon">&#128218;</span>
                <span class="tab-label">Lessons</span>
                <span class="tab-key">3</span>
            </button>
            <button class="tab" data-tab="quiz" role="tab" aria-selected="false" aria-controls="panel-quiz">
                <span class="tab-icon">&#10067;</span>
                <span class="tab-label">Quiz</span>
                <span class="tab-key">4</span>
            </button>
        </nav>

        <main class="content">
            <section id="panel-overview" class="panel active" role="tabpanel" aria-labelledby="tab-overview">
{overview_html}
            </section>

            <section id="panel-commands" class="panel" role="tabpanel" aria-labelledby="tab-commands">
{commands_html}
            </section>

            <section id="panel-lessons" class="panel" role="tabpanel" aria-labelledby="tab-lessons">
{lessons_html}
            </section>

            <section id="panel-quiz" class="panel" role="tabpanel" aria-labelledby="tab-quiz">
{quiz_html}
            </section>
        </main>

        <footer class="footer">
            <p>Learn Bash from Session Data | Press 1-4 to switch tabs</p>
        </footer>
    </div>

    <script>
{inline_js}
    </script>
</body>
</html>'''


def render_overview_tab(stats: dict[str, Any], commands: list[dict], categories: dict) -> str:
    """Render the overview/dashboard tab content."""
    total_commands = stats.get("total_commands", 0)
    unique_commands = stats.get("unique_commands", 0)
    unique_utilities = stats.get("unique_utilities", 0)
    date_range = stats.get("date_range", {"start": "N/A", "end": "N/A"})
    complexity_dist = stats.get("complexity_distribution", {"simple": 0, "intermediate": 0, "advanced": 0})

    # Calculate percentages for complexity bars
    total_for_pct = sum(complexity_dist.values()) or 1
    simple_pct = (complexity_dist.get("simple", 0) / total_for_pct) * 100
    intermediate_pct = (complexity_dist.get("intermediate", 0) / total_for_pct) * 100
    advanced_pct = (complexity_dist.get("advanced", 0) / total_for_pct) * 100

    # Top 10 commands by frequency - use pre-computed data if available
    top_commands_data = stats.get("top_commands", [])
    top_commands_html = ""

    if top_commands_data:
        max_freq = top_commands_data[0].get("count", 1) if top_commands_data else 1
        for item in top_commands_data[:10]:
            cmd_str = item.get("command", "")
            freq = item.get("count", 1)
            bar_width = (freq / max_freq) * 100
            # Extract base command from full command
            cmd_name = html.escape(cmd_str.split()[0] if cmd_str else "unknown")
            top_commands_html += f'''
                        <div class="top-command-item">
                            <div class="top-command-name">
                                <code class="cmd">{cmd_name}</code>
                            </div>
                            <div class="top-command-bar-container">
                                <div class="top-command-bar" style="width: {bar_width}%"></div>
                            </div>
                            <div class="top-command-count">{freq}</div>
                        </div>'''
    else:
        # Fallback to sorting commands by frequency
        sorted_commands = sorted(commands, key=lambda x: x.get("frequency", 0), reverse=True)[:10]
        max_freq = sorted_commands[0].get("frequency", 1) if sorted_commands else 1
        for cmd in sorted_commands:
            freq = cmd.get("frequency", 0)
            bar_width = (freq / max_freq) * 100
            cmd_name = html.escape(cmd.get("base_command", "unknown"))
            top_commands_html += f'''
                        <div class="top-command-item">
                            <div class="top-command-name">
                                <code class="cmd">{cmd_name}</code>
                            </div>
                            <div class="top-command-bar-container">
                                <div class="top-command-bar" style="width: {bar_width}%"></div>
                            </div>
                            <div class="top-command-count">{freq}</div>
                        </div>'''

    # New commands (first appearances)
    new_commands = [c for c in commands if c.get("is_new", False)][:8]
    new_commands_html = ""
    for cmd in new_commands:
        cmd_name = html.escape(cmd.get("base_command", "unknown"))
        first_seen = cmd.get("first_seen", "")
        new_commands_html += f'''
                        <div class="new-command-chip">
                            <code class="cmd">{cmd_name}</code>
                            <span class="first-seen">{first_seen}</span>
                        </div>'''

    if not new_commands_html:
        new_commands_html = '<p class="empty-state">No new commands detected in this session</p>'

    # Category breakdown for pie chart
    category_data = []
    cat_colors = [
        "#4285f4", "#ea4335", "#fbbc05", "#34a853", "#ff6d01",
        "#46bdc6", "#7baaf7", "#f07b72", "#fcd04f", "#81c995"
    ]
    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)[:8]

    for idx, (cat_name, cat_cmds) in enumerate(sorted_cats):
        color = cat_colors[idx % len(cat_colors)]
        count = len(cat_cmds)
        category_data.append({
            "name": cat_name,
            "count": count,
            "color": color
        })

    # Generate SVG pie chart
    pie_svg = _generate_pie_chart(category_data)

    # Category legend
    category_legend = ""
    for cat in category_data:
        category_legend += f'''
                        <div class="legend-item">
                            <span class="legend-color" style="background: {cat['color']}"></span>
                            <span class="legend-label">{html.escape(cat['name'])}</span>
                            <span class="legend-count">{cat['count']}</span>
                        </div>'''

    return f'''
                <div class="dashboard">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{total_commands}</div>
                            <div class="stat-label">Total Commands</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{unique_commands}</div>
                            <div class="stat-label">Unique Commands</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{unique_utilities}</div>
                            <div class="stat-label">Unique Utilities</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value date-value">{date_range.get("start", "N/A")}</div>
                            <div class="stat-label">to {date_range.get("end", "N/A")}</div>
                        </div>
                    </div>

                    <div class="charts-row">
                        <div class="chart-card">
                            <h3>Complexity Distribution</h3>
                            <div class="complexity-bars">
                                <div class="complexity-row">
                                    <span class="complexity-label simple">Simple</span>
                                    <div class="complexity-bar-bg">
                                        <div class="complexity-bar simple" style="width: {simple_pct}%"></div>
                                    </div>
                                    <span class="complexity-count">{complexity_dist.get("simple", 0)}</span>
                                </div>
                                <div class="complexity-row">
                                    <span class="complexity-label intermediate">Intermediate</span>
                                    <div class="complexity-bar-bg">
                                        <div class="complexity-bar intermediate" style="width: {intermediate_pct}%"></div>
                                    </div>
                                    <span class="complexity-count">{complexity_dist.get("intermediate", 0)}</span>
                                </div>
                                <div class="complexity-row">
                                    <span class="complexity-label advanced">Advanced</span>
                                    <div class="complexity-bar-bg">
                                        <div class="complexity-bar advanced" style="width: {advanced_pct}%"></div>
                                    </div>
                                    <span class="complexity-count">{complexity_dist.get("advanced", 0)}</span>
                                </div>
                            </div>
                        </div>

                        <div class="chart-card">
                            <h3>Category Breakdown</h3>
                            <div class="pie-container">
                                {pie_svg}
                                <div class="category-legend">
                                    {category_legend}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="charts-row">
                        <div class="chart-card wide">
                            <h3>Top 10 Most-Used Commands</h3>
                            <div class="top-commands">
                                {top_commands_html}
                            </div>
                        </div>

                        <div class="chart-card">
                            <h3>New Commands</h3>
                            <div class="new-commands">
                                {new_commands_html}
                            </div>
                        </div>
                    </div>
                </div>'''


def _generate_pie_chart(category_data: list[dict]) -> str:
    """Generate an SVG pie chart."""
    if not category_data:
        return '<div class="empty-state">No category data</div>'

    total = sum(c["count"] for c in category_data)
    if total == 0:
        return '<div class="empty-state">No commands to display</div>'

    # SVG pie chart
    cx, cy, r = 80, 80, 70
    paths = []
    current_angle = -90  # Start from top

    for cat in category_data:
        pct = cat["count"] / total
        angle = pct * 360

        # Calculate arc
        start_rad = current_angle * 3.14159 / 180
        end_rad = (current_angle + angle) * 3.14159 / 180

        x1 = cx + r * (end_rad - start_rad > 0 and 1 or -1) * __import__('math').cos(start_rad)
        y1 = cy + r * __import__('math').sin(start_rad)
        x2 = cx + r * __import__('math').cos(end_rad)
        y2 = cy + r * __import__('math').sin(end_rad)

        large_arc = 1 if angle > 180 else 0

        # Create path
        import math
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)

        path = f'M {cx} {cy} L {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z'
        paths.append(f'<path d="{path}" fill="{cat["color"]}" stroke="#fff" stroke-width="2"><title>{html.escape(cat["name"])}: {cat["count"]}</title></path>')

        current_angle += angle

    return f'''<svg viewBox="0 0 160 160" class="pie-chart">
                                    {''.join(paths)}
                                </svg>'''


def render_commands_tab(commands: list[dict]) -> str:
    """Render the commands reference tab."""
    # Group by category for filter chips
    categories_set = set()
    for cmd in commands:
        categories_set.add(cmd.get("category", "Other"))

    category_chips = ""
    for cat in sorted(categories_set):
        category_chips += f'<button class="filter-chip" data-category="{html.escape(cat)}">{html.escape(cat)}</button>'

    # Generate command cards
    commands_html = ""
    for idx, cmd in enumerate(commands):
        cmd_id = f"cmd-{idx}"
        base_cmd = html.escape(cmd.get("base_command", "unknown"))
        full_cmd = html.escape(cmd.get("full_command", ""))
        category = html.escape(cmd.get("category", "Other"))
        complexity = cmd.get("complexity", "simple")
        frequency = cmd.get("frequency", 0)
        description = html.escape(cmd.get("description", "No description available"))

        # Syntax highlighted command
        highlighted = _syntax_highlight(cmd.get("full_command", ""))

        # Flags breakdown
        flags = cmd.get("flags", [])
        flags_html = ""
        if flags:
            flags_html = '<div class="flags-section"><h5>Flags:</h5><ul class="flags-list">'
            for flag in flags:
                flag_name = html.escape(flag.get("flag", ""))
                flag_desc = html.escape(flag.get("description", ""))
                flags_html += f'<li><code class="flag">{flag_name}</code> - {flag_desc}</li>'
            flags_html += '</ul></div>'

        # Output preview
        output_preview = cmd.get("output_preview", "")
        output_html = ""
        if output_preview:
            output_html = f'''
                            <div class="output-section">
                                <h5>Example Output:</h5>
                                <pre class="output-preview">{html.escape(output_preview)}</pre>
                            </div>'''

        commands_html += f'''
                        <div class="command-card" data-category="{category}" data-complexity="{complexity}" data-frequency="{frequency}" data-name="{base_cmd}">
                            <div class="command-header" onclick="toggleCommand('{cmd_id}')">
                                <div class="command-main">
                                    <code class="cmd">{base_cmd}</code>
                                    <span class="complexity-badge {complexity}">{complexity}</span>
                                    <span class="category-badge">{category}</span>
                                </div>
                                <div class="command-meta">
                                    <span class="frequency">Used {frequency}x</span>
                                    <span class="expand-icon">&#9660;</span>
                                </div>
                            </div>
                            <div class="command-details" id="{cmd_id}">
                                <div class="full-command">
                                    <h5>Full Command:</h5>
                                    <pre class="syntax-highlighted">{highlighted}</pre>
                                </div>
                                <div class="description">
                                    <h5>Description:</h5>
                                    <p>{description}</p>
                                </div>
                                {flags_html}
                                {output_html}
                            </div>
                        </div>'''

    return f'''
                <div class="commands-container">
                    <div class="commands-toolbar">
                        <div class="search-box">
                            <input type="text" id="command-search" placeholder="Search commands..." oninput="filterCommands()">
                        </div>
                        <div class="sort-controls">
                            <label>Sort by:</label>
                            <select id="sort-select" onchange="sortCommands()">
                                <option value="frequency">Frequency</option>
                                <option value="complexity">Complexity</option>
                                <option value="category">Category</option>
                                <option value="name">Alphabetical</option>
                            </select>
                        </div>
                    </div>

                    <div class="filter-chips">
                        <button class="filter-chip active" data-category="all">All</button>
                        {category_chips}
                    </div>

                    <div class="commands-list" id="commands-list">
                        {commands_html}
                    </div>
                </div>'''


def _syntax_highlight(command: str) -> str:
    """Apply syntax highlighting to a bash command."""
    if not command:
        return ""

    import re

    # Escape HTML first
    escaped = html.escape(command)

    # Patterns for highlighting (order matters)
    patterns = [
        # Strings (single and double quoted)
        (r'(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)', r'<span class="string">\1</span>'),
        # Paths (starting with / or ./ or ~/)
        (r'(\s|^)((?:/[\w.-]+)+|\.{1,2}/[\w./-]*|~/[\w./-]*)', r'\1<span class="path">\2</span>'),
        # Flags (long and short)
        (r'(\s)(--?[\w-]+)', r'\1<span class="flag">\2</span>'),
        # Operators and redirects
        (r'(\||&amp;&amp;|&gt;|&lt;|&gt;&gt;|\$\(|\))', r'<span class="operator">\1</span>'),
        # Variables
        (r'(\$[\w{}]+)', r'<span class="variable">\1</span>'),
    ]

    result = escaped
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    # Highlight the base command (first word)
    result = re.sub(r'^([\w.-]+)', r'<span class="cmd">\1</span>', result)

    return result


def render_lessons_tab(categories: dict, commands: list[dict]) -> str:
    """Render the categorized lessons tab."""
    if not categories:
        return '<div class="empty-state">No categories found in the session data</div>'

    # Sort categories by command count
    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)

    lessons_html = ""
    for cat_name, cat_commands in sorted_cats:
        if not cat_commands:
            continue

        # Get full command data for this category
        cat_cmd_data = [c for c in commands if c.get("category") == cat_name]

        # Concept overview based on category
        concept = _get_category_concept(cat_name)

        # Commands in this category
        cat_commands_html = ""
        for cmd in cat_cmd_data[:10]:  # Limit to 10 per category
            base_cmd = html.escape(cmd.get("base_command", ""))
            description = html.escape(cmd.get("description", ""))
            complexity = cmd.get("complexity", "simple")
            highlighted = _syntax_highlight(cmd.get("full_command", ""))

            cat_commands_html += f'''
                            <div class="lesson-command">
                                <div class="lesson-command-header">
                                    <code class="cmd">{base_cmd}</code>
                                    <span class="complexity-badge {complexity}">{complexity}</span>
                                </div>
                                <pre class="syntax-highlighted">{highlighted}</pre>
                                <p class="lesson-description">{description}</p>
                            </div>'''

        # Patterns observed
        patterns = _extract_patterns(cat_cmd_data)
        patterns_html = ""
        if patterns:
            patterns_html = '<div class="patterns"><h4>Patterns Observed:</h4><ul>'
            for pattern in patterns:
                patterns_html += f'<li>{html.escape(pattern)}</li>'
            patterns_html += '</ul></div>'

        lessons_html += f'''
                    <div class="lesson-section">
                        <h2 class="lesson-title">
                            <span class="lesson-icon">{_get_category_icon(cat_name)}</span>
                            {html.escape(cat_name)}
                            <span class="lesson-count">({len(cat_commands)} commands)</span>
                        </h2>
                        <div class="lesson-content">
                            <div class="concept-overview">
                                <h4>Concept Overview:</h4>
                                <p>{html.escape(concept)}</p>
                            </div>
                            <div class="lesson-commands">
                                <h4>Commands:</h4>
                                {cat_commands_html}
                            </div>
                            {patterns_html}
                        </div>
                    </div>'''

    return f'''
                <div class="lessons-container">
                    {lessons_html}
                </div>'''


def _get_category_concept(category: str) -> str:
    """Get concept overview for a category."""
    concepts = {
        "File Management": "Commands for creating, copying, moving, deleting, and organizing files and directories in the filesystem.",
        "Text Processing": "Tools for searching, filtering, transforming, and manipulating text content in files and streams.",
        "System Administration": "Commands for managing system resources, processes, users, and system configuration.",
        "Network": "Utilities for network communication, file transfer, and connectivity diagnostics.",
        "Package Management": "Tools for installing, updating, and managing software packages on the system.",
        "Version Control": "Git and other version control commands for tracking changes and collaborating on code.",
        "Process Management": "Commands for viewing, controlling, and managing running processes.",
        "User Management": "Tools for managing user accounts, permissions, and access control.",
        "Disk Management": "Utilities for managing disk space, partitions, and storage devices.",
        "Shell Scripting": "Built-in shell commands and constructs for scripting and automation.",
        "Development": "Programming tools, compilers, interpreters, and development utilities.",
        "Compression": "Tools for compressing, archiving, and extracting files.",
        "Search": "Commands for finding files, searching content, and locating resources.",
        "Permissions": "Tools for managing file permissions, ownership, and access control.",
    }
    return concepts.get(category, f"Commands related to {category.lower()} operations and utilities.")


def _get_category_icon(category: str) -> str:
    """Get icon for a category."""
    icons = {
        "File Management": "&#128193;",
        "Text Processing": "&#128196;",
        "System Administration": "&#9881;",
        "Network": "&#127760;",
        "Package Management": "&#128230;",
        "Version Control": "&#128202;",
        "Process Management": "&#9654;",
        "User Management": "&#128100;",
        "Disk Management": "&#128191;",
        "Shell Scripting": "&#10095;",
        "Development": "&#128187;",
        "Compression": "&#128230;",
        "Search": "&#128269;",
        "Permissions": "&#128274;",
    }
    return icons.get(category, "&#128204;")


def _extract_patterns(commands: list[dict]) -> list[str]:
    """Extract common patterns from a list of commands."""
    patterns = []

    # Check for piping patterns
    piped = [c for c in commands if "|" in c.get("full_command", "")]
    if piped:
        patterns.append(f"Piping output between commands ({len(piped)} instances)")

    # Check for redirection
    redirected = [c for c in commands if any(r in c.get("full_command", "") for r in [">", ">>", "<"])]
    if redirected:
        patterns.append(f"Output/input redirection ({len(redirected)} instances)")

    # Check for flag usage
    with_flags = [c for c in commands if c.get("flags")]
    if with_flags:
        common_flags = {}
        for cmd in with_flags:
            for flag in cmd.get("flags", []):
                f = flag.get("flag", "")
                common_flags[f] = common_flags.get(f, 0) + 1
        if common_flags:
            top_flag = max(common_flags.items(), key=lambda x: x[1])
            if top_flag[1] > 1:
                patterns.append(f"Common flag: {top_flag[0]} (used {top_flag[1]} times)")

    # Check for glob patterns
    globbed = [c for c in commands if any(g in c.get("full_command", "") for g in ["*", "?", "["])]
    if globbed:
        patterns.append(f"Glob/wildcard patterns ({len(globbed)} instances)")

    return patterns[:4]  # Limit to 4 patterns


def render_quiz_tab(quizzes: list[dict]) -> str:
    """Render the quiz tab."""
    if not quizzes:
        return '''
                <div class="quiz-container">
                    <div class="empty-state">No quiz questions available</div>
                </div>'''

    questions_html = ""
    for idx, quiz in enumerate(quizzes):
        q_id = f"q{idx}"
        question = html.escape(quiz.get("question", ""))
        options = quiz.get("options", [])
        correct = quiz.get("correct_answer", 0)
        explanation = html.escape(quiz.get("explanation", ""))

        options_html = ""
        for opt_idx, option in enumerate(options):
            opt_letter = chr(65 + opt_idx)  # A, B, C, D
            options_html += f'''
                            <label class="quiz-option" data-question="{q_id}" data-index="{opt_idx}">
                                <input type="radio" name="{q_id}" value="{opt_idx}" onchange="checkAnswer('{q_id}', {opt_idx}, {correct})">
                                <span class="option-letter">{opt_letter}</span>
                                <span class="option-text">{html.escape(option)}</span>
                            </label>'''

        questions_html += f'''
                    <div class="quiz-question" id="question-{q_id}">
                        <div class="question-number">Question {idx + 1}</div>
                        <div class="question-text">{question}</div>
                        <div class="quiz-options">
                            {options_html}
                        </div>
                        <div class="quiz-feedback" id="feedback-{q_id}">
                            <div class="feedback-result"></div>
                            <div class="feedback-explanation">{explanation}</div>
                        </div>
                    </div>'''

    return f'''
                <div class="quiz-container">
                    <div class="quiz-header">
                        <h2>Test Your Knowledge</h2>
                        <p>Answer the following questions to test your understanding of the bash commands.</p>
                        <div class="quiz-score">
                            <span>Score: </span>
                            <span id="score-current">0</span>
                            <span> / </span>
                            <span id="score-total">{len(quizzes)}</span>
                        </div>
                    </div>

                    <div class="quiz-questions">
                        {questions_html}
                    </div>

                    <div class="quiz-actions">
                        <button class="btn btn-secondary" onclick="resetQuiz()">Try Again</button>
                    </div>
                </div>'''


def get_inline_css() -> str:
    """Return all CSS styles."""
    return '''
        /* CSS Reset and Base */
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --text-muted: #adb5bd;
            --border-color: #dee2e6;
            --accent-primary: #4285f4;
            --accent-success: #34a853;
            --accent-warning: #fbbc05;
            --accent-danger: #ea4335;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --transition-fast: 150ms ease;
            --transition-normal: 250ms ease;
        }

        [data-theme="dark"] {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-tertiary: #0f3460;
            --text-primary: #eaeaea;
            --text-secondary: #a0a0a0;
            --text-muted: #666666;
            --border-color: #2d2d4a;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.3);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.4);
        }

        html {
            font-size: 16px;
            scroll-behavior: smooth;
        }

        body {
            font-family: var(--font-sans);
            background: var(--bg-secondary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 32px;
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 4px;
        }

        .theme-toggle {
            background: var(--bg-tertiary);
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition-fast);
        }

        .theme-toggle:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-sm);
        }

        .theme-icon {
            font-size: 1.25rem;
        }

        .dark-icon { display: none; }
        [data-theme="dark"] .light-icon { display: none; }
        [data-theme="dark"] .dark-icon { display: inline; }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 8px;
            padding: 8px;
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
            margin-bottom: 20px;
        }

        .tab {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 20px;
            background: transparent;
            border: none;
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition-fast);
            position: relative;
        }

        .tab:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .tab.active {
            background: var(--accent-primary);
            color: white;
        }

        .tab-icon {
            font-size: 1.1rem;
        }

        .tab-key {
            position: absolute;
            top: 4px;
            right: 8px;
            font-size: 0.7rem;
            opacity: 0.5;
            font-family: var(--font-mono);
        }

        /* Content Panels */
        .content {
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            min-height: 500px;
        }

        .panel {
            display: none;
            padding: 32px;
            animation: fadeIn 0.3s ease;
        }

        .panel.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Dashboard / Overview */
        .dashboard {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }

        .stat-card {
            background: var(--bg-secondary);
            padding: 24px;
            border-radius: var(--radius-md);
            text-align: center;
            transition: var(--transition-fast);
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent-primary);
            line-height: 1.2;
        }

        .stat-value.date-value {
            font-size: 1rem;
            font-family: var(--font-mono);
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 8px;
        }

        .charts-row {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
        }

        .chart-card {
            background: var(--bg-secondary);
            padding: 24px;
            border-radius: var(--radius-md);
        }

        .chart-card.wide {
            grid-column: span 1;
        }

        .chart-card h3 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--text-primary);
        }

        /* Complexity Bars */
        .complexity-bars {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .complexity-row {
            display: grid;
            grid-template-columns: 100px 1fr 50px;
            align-items: center;
            gap: 12px;
        }

        .complexity-label {
            font-size: 0.85rem;
            font-weight: 500;
        }

        .complexity-label.simple { color: var(--accent-success); }
        .complexity-label.intermediate { color: var(--accent-warning); }
        .complexity-label.advanced { color: var(--accent-danger); }

        .complexity-bar-bg {
            height: 24px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            overflow: hidden;
        }

        .complexity-bar {
            height: 100%;
            border-radius: var(--radius-sm);
            transition: width 0.5s ease;
        }

        .complexity-bar.simple { background: var(--accent-success); }
        .complexity-bar.intermediate { background: var(--accent-warning); }
        .complexity-bar.advanced { background: var(--accent-danger); }

        .complexity-count {
            font-size: 0.9rem;
            font-weight: 600;
            text-align: right;
            color: var(--text-secondary);
        }

        /* Pie Chart */
        .pie-container {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        .pie-chart {
            width: 160px;
            height: 160px;
            flex-shrink: 0;
        }

        .category-legend {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
        }

        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 2px;
            flex-shrink: 0;
        }

        .legend-label {
            flex: 1;
            color: var(--text-primary);
        }

        .legend-count {
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* Top Commands */
        .top-commands {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .top-command-item {
            display: grid;
            grid-template-columns: 120px 1fr 50px;
            align-items: center;
            gap: 12px;
        }

        .top-command-name code {
            font-size: 0.85rem;
        }

        .top-command-bar-container {
            height: 20px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            overflow: hidden;
        }

        .top-command-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), #7baaf7);
            border-radius: var(--radius-sm);
            transition: width 0.5s ease;
        }

        .top-command-count {
            font-size: 0.9rem;
            font-weight: 600;
            text-align: right;
            color: var(--text-secondary);
        }

        /* New Commands */
        .new-commands {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }

        .new-command-chip {
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 12px 16px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-md);
            border-left: 3px solid var(--accent-success);
        }

        .new-command-chip code {
            font-size: 0.9rem;
        }

        .first-seen {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Commands Tab */
        .commands-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .commands-toolbar {
            display: flex;
            gap: 16px;
            align-items: center;
        }

        .search-box {
            flex: 1;
        }

        .search-box input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border-color);
            border-radius: var(--radius-md);
            font-size: 0.95rem;
            background: var(--bg-secondary);
            color: var(--text-primary);
            transition: var(--transition-fast);
        }

        .search-box input:focus {
            outline: none;
            border-color: var(--accent-primary);
        }

        .sort-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sort-controls label {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .sort-controls select {
            padding: 10px 14px;
            border: 2px solid var(--border-color);
            border-radius: var(--radius-md);
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 0.9rem;
            cursor: pointer;
        }

        .filter-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .filter-chip {
            padding: 8px 16px;
            border: 2px solid var(--border-color);
            border-radius: 20px;
            background: transparent;
            color: var(--text-secondary);
            font-size: 0.85rem;
            cursor: pointer;
            transition: var(--transition-fast);
        }

        .filter-chip:hover {
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }

        .filter-chip.active {
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: white;
        }

        .commands-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .command-card {
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            overflow: hidden;
            transition: var(--transition-fast);
        }

        .command-card:hover {
            box-shadow: var(--shadow-sm);
        }

        .command-card.hidden {
            display: none;
        }

        .command-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            background: var(--bg-secondary);
            cursor: pointer;
            transition: var(--transition-fast);
        }

        .command-header:hover {
            background: var(--bg-tertiary);
        }

        .command-main {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .command-meta {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .frequency {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .expand-icon {
            color: var(--text-muted);
            transition: transform var(--transition-fast);
        }

        .command-card.expanded .expand-icon {
            transform: rotate(180deg);
        }

        .command-details {
            display: none;
            padding: 20px;
            border-top: 1px solid var(--border-color);
            background: var(--bg-primary);
        }

        .command-details.show {
            display: block;
        }

        .command-details h5 {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .command-details > div {
            margin-bottom: 20px;
        }

        .command-details > div:last-child {
            margin-bottom: 0;
        }

        .flags-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .flags-list li {
            display: flex;
            align-items: baseline;
            gap: 8px;
            font-size: 0.9rem;
        }

        .output-preview {
            background: var(--bg-secondary);
            padding: 16px;
            border-radius: var(--radius-md);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            overflow-x: auto;
            white-space: pre-wrap;
        }

        /* Syntax Highlighting */
        code, pre {
            font-family: var(--font-mono);
        }

        code.cmd, .syntax-highlighted .cmd {
            color: #4285f4;
            font-weight: 600;
        }

        code.flag, .syntax-highlighted .flag {
            color: #34a853;
        }

        .syntax-highlighted .string {
            color: #ff6d01;
        }

        .syntax-highlighted .operator {
            color: #9c27b0;
            font-weight: 600;
        }

        .syntax-highlighted .path {
            color: #6c757d;
        }

        .syntax-highlighted .variable {
            color: #ea4335;
        }

        .syntax-highlighted {
            background: var(--bg-secondary);
            padding: 12px 16px;
            border-radius: var(--radius-md);
            font-size: 0.9rem;
            overflow-x: auto;
            white-space: pre-wrap;
        }

        /* Badges */
        .complexity-badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .complexity-badge.simple {
            background: rgba(52, 168, 83, 0.15);
            color: var(--accent-success);
        }

        .complexity-badge.intermediate {
            background: rgba(251, 188, 5, 0.15);
            color: #d49a00;
        }

        .complexity-badge.advanced {
            background: rgba(234, 67, 53, 0.15);
            color: var(--accent-danger);
        }

        .category-badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            background: var(--bg-tertiary);
            color: var(--text-secondary);
        }

        /* Lessons Tab */
        .lessons-container {
            display: flex;
            flex-direction: column;
            gap: 32px;
        }

        .lesson-section {
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }

        .lesson-title {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px 24px;
            background: var(--bg-secondary);
            font-size: 1.25rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
        }

        .lesson-icon {
            font-size: 1.5rem;
        }

        .lesson-count {
            font-size: 0.9rem;
            font-weight: 400;
            color: var(--text-secondary);
            margin-left: auto;
        }

        .lesson-content {
            padding: 24px;
        }

        .concept-overview {
            margin-bottom: 24px;
            padding: 16px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            border-left: 4px solid var(--accent-primary);
        }

        .concept-overview h4 {
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--accent-primary);
        }

        .concept-overview p {
            color: var(--text-secondary);
            line-height: 1.7;
        }

        .lesson-commands h4 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 16px;
        }

        .lesson-command {
            padding: 16px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            margin-bottom: 12px;
        }

        .lesson-command:last-child {
            margin-bottom: 0;
        }

        .lesson-command-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .lesson-description {
            margin-top: 12px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .patterns {
            margin-top: 24px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
        }

        .patterns h4 {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 12px;
        }

        .patterns ul {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .patterns li {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .patterns li::before {
            content: "\\2022";
            color: var(--accent-primary);
            font-weight: bold;
        }

        /* Quiz Tab */
        .quiz-container {
            max-width: 800px;
            margin: 0 auto;
        }

        .quiz-header {
            text-align: center;
            margin-bottom: 32px;
        }

        .quiz-header h2 {
            font-size: 1.5rem;
            margin-bottom: 8px;
        }

        .quiz-header p {
            color: var(--text-secondary);
            margin-bottom: 20px;
        }

        .quiz-score {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 12px 24px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            font-size: 1.1rem;
            font-weight: 600;
        }

        #score-current {
            color: var(--accent-primary);
        }

        .quiz-questions {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .quiz-question {
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            padding: 24px;
        }

        .question-number {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--accent-primary);
            margin-bottom: 8px;
        }

        .question-text {
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 20px;
            line-height: 1.5;
        }

        .quiz-options {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .quiz-option {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            background: var(--bg-primary);
            border: 2px solid var(--border-color);
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: var(--transition-fast);
        }

        .quiz-option:hover {
            border-color: var(--accent-primary);
        }

        .quiz-option input {
            display: none;
        }

        .option-letter {
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-tertiary);
            border-radius: 50%;
            font-size: 0.85rem;
            font-weight: 600;
            flex-shrink: 0;
        }

        .option-text {
            flex: 1;
        }

        .quiz-option.correct {
            border-color: var(--accent-success);
            background: rgba(52, 168, 83, 0.1);
        }

        .quiz-option.correct .option-letter {
            background: var(--accent-success);
            color: white;
        }

        .quiz-option.incorrect {
            border-color: var(--accent-danger);
            background: rgba(234, 67, 53, 0.1);
        }

        .quiz-option.incorrect .option-letter {
            background: var(--accent-danger);
            color: white;
        }

        .quiz-option.disabled {
            pointer-events: none;
            opacity: 0.7;
        }

        .quiz-feedback {
            display: none;
            margin-top: 16px;
            padding: 16px;
            border-radius: var(--radius-md);
        }

        .quiz-feedback.show {
            display: block;
        }

        .quiz-feedback.correct {
            background: rgba(52, 168, 83, 0.1);
            border-left: 4px solid var(--accent-success);
        }

        .quiz-feedback.incorrect {
            background: rgba(234, 67, 53, 0.1);
            border-left: 4px solid var(--accent-danger);
        }

        .feedback-result {
            font-weight: 600;
            margin-bottom: 8px;
        }

        .feedback-explanation {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .quiz-actions {
            display: flex;
            justify-content: center;
            margin-top: 32px;
        }

        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: var(--radius-md);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-fast);
        }

        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .btn-secondary:hover {
            background: var(--border-color);
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 48px 24px;
            color: var(--text-secondary);
        }

        /* Print Styles */
        @media print {
            body {
                background: white;
                color: black;
            }

            .header, .tabs, .footer, .theme-toggle, .quiz-actions {
                display: none;
            }

            .content {
                box-shadow: none;
            }

            .panel {
                display: block !important;
                page-break-inside: avoid;
            }

            .panel::before {
                content: attr(aria-labelledby);
                display: block;
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #333;
            }

            .command-details {
                display: block !important;
            }
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .charts-row {
                grid-template-columns: 1fr;
            }

            .pie-container {
                flex-direction: column;
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 12px;
            }

            .header {
                padding: 16px 20px;
            }

            .header h1 {
                font-size: 1.25rem;
            }

            .tab-label {
                display: none;
            }

            .tab {
                padding: 12px;
            }

            .tab-icon {
                font-size: 1.25rem;
            }

            .panel {
                padding: 20px;
            }

            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }

            .stat-value {
                font-size: 1.75rem;
            }

            .commands-toolbar {
                flex-direction: column;
            }

            .command-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }

            .command-meta {
                width: 100%;
                justify-content: space-between;
            }
        }
'''


def get_inline_js(quizzes: list[dict]) -> str:
    """Return all JavaScript code."""
    quiz_data = json.dumps(quizzes)

    return f'''
        // Quiz data
        const quizData = {quiz_data};
        let score = 0;
        let answeredQuestions = new Set();

        // Tab Navigation
        document.querySelectorAll('.tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                switchTab(tab.dataset.tab);
            }});
        }});

        function switchTab(tabName) {{
            // Update tabs
            document.querySelectorAll('.tab').forEach(t => {{
                t.classList.remove('active');
                t.setAttribute('aria-selected', 'false');
            }});
            document.querySelector(`[data-tab="${{tabName}}"]`).classList.add('active');
            document.querySelector(`[data-tab="${{tabName}}"]`).setAttribute('aria-selected', 'true');

            // Update panels
            document.querySelectorAll('.panel').forEach(p => {{
                p.classList.remove('active');
            }});
            document.getElementById(`panel-${{tabName}}`).classList.add('active');
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            const tabs = ['overview', 'commands', 'lessons', 'quiz'];
            const key = e.key;

            if (key >= '1' && key <= '4') {{
                e.preventDefault();
                switchTab(tabs[parseInt(key) - 1]);
            }}
        }});

        // Theme Toggle
        function toggleTheme() {{
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }}

        // Load saved theme
        (function() {{
            const savedTheme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', savedTheme);
        }})();

        // Command expansion
        function toggleCommand(cmdId) {{
            const details = document.getElementById(cmdId);
            const card = details.closest('.command-card');

            details.classList.toggle('show');
            card.classList.toggle('expanded');
        }}

        // Command filtering
        function filterCommands() {{
            const searchTerm = document.getElementById('command-search').value.toLowerCase();
            const activeCategory = document.querySelector('.filter-chip.active').dataset.category;

            document.querySelectorAll('.command-card').forEach(card => {{
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category;

                const matchesSearch = name.includes(searchTerm);
                const matchesCategory = activeCategory === 'all' || category === activeCategory;

                card.classList.toggle('hidden', !(matchesSearch && matchesCategory));
            }});
        }}

        // Category filter chips
        document.querySelectorAll('.filter-chip').forEach(chip => {{
            chip.addEventListener('click', () => {{
                document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                filterCommands();
            }});
        }});

        // Command sorting
        function sortCommands() {{
            const sortBy = document.getElementById('sort-select').value;
            const list = document.getElementById('commands-list');
            const cards = Array.from(list.querySelectorAll('.command-card'));

            cards.sort((a, b) => {{
                switch(sortBy) {{
                    case 'frequency':
                        return parseInt(b.dataset.frequency) - parseInt(a.dataset.frequency);
                    case 'complexity':
                        const order = {{'simple': 1, 'intermediate': 2, 'advanced': 3}};
                        return order[a.dataset.complexity] - order[b.dataset.complexity];
                    case 'category':
                        return a.dataset.category.localeCompare(b.dataset.category);
                    case 'name':
                        return a.dataset.name.localeCompare(b.dataset.name);
                    default:
                        return 0;
                }}
            }});

            cards.forEach(card => list.appendChild(card));
        }}

        // Quiz functions
        function checkAnswer(questionId, selectedIndex, correctIndex) {{
            if (answeredQuestions.has(questionId)) return;
            answeredQuestions.add(questionId);

            const question = document.getElementById(`question-${{questionId}}`);
            const options = question.querySelectorAll('.quiz-option');
            const feedback = document.getElementById(`feedback-${{questionId}}`);

            const isCorrect = selectedIndex === correctIndex;

            // Mark options
            options.forEach((opt, idx) => {{
                opt.classList.add('disabled');
                if (idx === correctIndex) {{
                    opt.classList.add('correct');
                }} else if (idx === selectedIndex && !isCorrect) {{
                    opt.classList.add('incorrect');
                }}
            }});

            // Show feedback
            feedback.classList.add('show');
            feedback.classList.add(isCorrect ? 'correct' : 'incorrect');
            feedback.querySelector('.feedback-result').textContent = isCorrect ? 'Correct!' : 'Incorrect';

            // Update score
            if (isCorrect) {{
                score++;
                document.getElementById('score-current').textContent = score;
            }}
        }}

        function resetQuiz() {{
            score = 0;
            answeredQuestions.clear();
            document.getElementById('score-current').textContent = '0';

            document.querySelectorAll('.quiz-question').forEach(q => {{
                q.querySelectorAll('.quiz-option').forEach(opt => {{
                    opt.classList.remove('correct', 'incorrect', 'disabled');
                    opt.querySelector('input').checked = false;
                }});

                const feedback = q.querySelector('.quiz-feedback');
                feedback.classList.remove('show', 'correct', 'incorrect');
            }});
        }}

        // Smooth scrolling for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function(e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    '''


def generate_html_files(
    commands: List[dict],
    analysis: dict,
    quizzes: list,
    output_dir: Path
) -> List[Path]:
    """
    Generate HTML files from commands, analysis and quizzes.

    This is the interface expected by main.py for the pipeline.

    Args:
        commands: List of command dictionaries
        analysis: Analysis dictionary from analyze_commands
        quizzes: List of quiz dictionaries
        output_dir: Output directory path

    Returns:
        List of generated file paths
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build analysis_result in expected format for generate_html
    stats = analysis.get('statistics', {})
    categories = analysis.get('categories', {})
    analyzed_commands = analysis.get('commands', commands)

    # Build frequency map from top_commands
    top_commands_data = analysis.get('top_commands', [])
    frequency_map = {}
    for item in top_commands_data:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            cmd_str, count = item[0], item[1]
            frequency_map[cmd_str] = count

    # Map complexity scores (1-5) to string labels for CSS
    def complexity_to_label(score):
        if score <= 2:
            return 'simple'
        elif score == 3:
            return 'intermediate'
        else:
            return 'advanced'

    # Transform commands to expected format
    formatted_commands = []
    for cmd in analyzed_commands:
        # Convert flags to expected format (list of dicts with 'flag' and 'description')
        raw_flags = cmd.get('flags', [])
        formatted_flags = []
        for f in raw_flags:
            if isinstance(f, dict):
                formatted_flags.append(f)
            elif isinstance(f, str):
                formatted_flags.append({'flag': f, 'description': ''})

        cmd_str = cmd.get('command', '')
        complexity_score = cmd.get('complexity', 1)

        formatted_commands.append({
            'base_command': cmd.get('base_command', cmd_str.split()[0] if cmd_str else ''),
            'full_command': cmd_str,
            'category': cmd.get('category', 'Other'),
            'complexity': complexity_to_label(complexity_score),
            'complexity_score': complexity_score,
            'frequency': frequency_map.get(cmd_str, 1),
            'description': cmd.get('description', ''),
            'flags': formatted_flags,
            'is_new': False,
        })

    # Transform complexity distribution from numeric keys to string labels
    raw_complexity = stats.get('complexity_distribution', {})
    complexity_distribution = {
        'simple': raw_complexity.get(1, 0) + raw_complexity.get(2, 0),
        'intermediate': raw_complexity.get(3, 0),
        'advanced': raw_complexity.get(4, 0) + raw_complexity.get(5, 0),
    }

    # Build top commands list with proper frequencies
    top_10_commands = []
    for item in top_commands_data[:10]:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            top_10_commands.append({
                'command': item[0],
                'count': item[1]
            })

    analysis_result = {
        'stats': {
            'total_commands': stats.get('total_commands', len(commands)),
            'unique_commands': stats.get('unique_commands', len(commands)),
            'unique_utilities': stats.get('unique_base_commands', 0),
            'total_categories': len(categories),
            'complexity_avg': stats.get('average_complexity', 2),
            'complexity_distribution': complexity_distribution,
            'top_commands': top_10_commands,  # Pre-computed top commands with frequencies
        },
        'commands': formatted_commands,
        'categories': {cat: [c.get('command', '') for c in cmds] for cat, cmds in categories.items()},
    }

    # Transform quizzes to expected format for HTML generator
    # HTML generator expects: options as list of strings, correct_answer as int index
    formatted_quizzes = []
    for quiz in quizzes:
        options = quiz.get('options', [])

        # Convert options from dicts to strings and find correct index
        option_texts = []
        correct_idx = 0
        for idx, opt in enumerate(options):
            if isinstance(opt, dict):
                option_texts.append(opt.get('text', ''))
                if opt.get('is_correct', False):
                    correct_idx = idx
            else:
                option_texts.append(str(opt))

        formatted_quizzes.append({
            'question': quiz.get('question', ''),
            'options': option_texts,
            'correct_answer': correct_idx,
            'explanation': quiz.get('explanation', ''),
        })

    # Generate HTML
    html_content = _generate_html_impl(analysis_result, formatted_quizzes)

    # Write to file
    index_file = output_dir / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return [index_file]


def generate_html(
    commands_or_analysis: Any,
    analysis_or_quizzes: Any = None,
    quizzes: Any = None,
    output_dir: Any = None
) -> Any:
    """
    Wrapper that handles both original 2-param and main.py 4-param signatures.

    Original: generate_html(analysis_result, quizzes) -> str
    Pipeline: generate_html(commands, analysis, quizzes, output_dir) -> List[Path]
    """
    if output_dir is not None:
        # Called with 4 params from main.py pipeline
        return generate_html_files(commands_or_analysis, analysis_or_quizzes, quizzes, output_dir)
    elif quizzes is not None:
        # Called with 3 params (shouldn't happen but handle it)
        return generate_html_files(commands_or_analysis, analysis_or_quizzes, quizzes, Path('./output'))
    else:
        # Original 2-param call: generate_html(analysis_result, quizzes)
        return _generate_html_impl(commands_or_analysis, analysis_or_quizzes)


if __name__ == "__main__":
    # Test with sample data
    sample_analysis = {
        "stats": {
            "total_commands": 150,
            "unique_commands": 45,
            "unique_utilities": 28,
            "date_range": {"start": "2025-01-01", "end": "2025-02-05"},
            "complexity_distribution": {"simple": 80, "intermediate": 50, "advanced": 20}
        },
        "commands": [
            {
                "base_command": "ls",
                "full_command": "ls -la /home/user",
                "category": "File Management",
                "complexity": "simple",
                "frequency": 25,
                "description": "List directory contents with details",
                "flags": [{"flag": "-l", "description": "Long format"}, {"flag": "-a", "description": "Show hidden files"}],
                "is_new": False
            },
            {
                "base_command": "grep",
                "full_command": "grep -r 'pattern' ./src",
                "category": "Text Processing",
                "complexity": "intermediate",
                "frequency": 18,
                "description": "Search for patterns in files",
                "flags": [{"flag": "-r", "description": "Recursive search"}],
                "is_new": True,
                "first_seen": "2025-01-15"
            },
            {
                "base_command": "find",
                "full_command": "find . -name '*.py' -exec grep 'import' {} +",
                "category": "Search",
                "complexity": "advanced",
                "frequency": 8,
                "description": "Find files and execute commands on them",
                "flags": [{"flag": "-name", "description": "Match filename pattern"}, {"flag": "-exec", "description": "Execute command on results"}],
                "is_new": True,
                "first_seen": "2025-01-20"
            }
        ],
        "categories": {
            "File Management": ["ls", "cd", "mkdir", "cp", "mv"],
            "Text Processing": ["grep", "sed", "awk", "cat"],
            "Search": ["find", "locate"],
            "Network": ["curl", "wget"]
        }
    }

    sample_quizzes = [
        {
            "question": "What does the -l flag do in the 'ls' command?",
            "options": ["List only files", "Long format with details", "List hidden files", "List in reverse order"],
            "correct_answer": 1,
            "explanation": "The -l flag displays files in long format, showing permissions, owner, size, and modification date."
        },
        {
            "question": "Which command is used to search for text patterns in files?",
            "options": ["find", "grep", "locate", "which"],
            "correct_answer": 1,
            "explanation": "grep (Global Regular Expression Print) searches for text patterns in files using regular expressions."
        }
    ]

    html_output = generate_html(sample_analysis, sample_quizzes)
    print(f"Generated HTML length: {len(html_output)} characters")
    print("HTML generation complete!")
