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

try:
    from scripts.knowledge_base import COMMAND_DB, get_flags_for_command, get_command_info
except ImportError:
    try:
        from knowledge_base import COMMAND_DB, get_flags_for_command, get_command_info
    except ImportError:
        COMMAND_DB = {}
        def get_flags_for_command(cmd): return {}
        def get_command_info(cmd): return None


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


def _generate_operators_html(operators_used: dict, operator_descriptions: dict) -> str:
    """Generate HTML for the operators used section."""
    if not operators_used:
        return '<p class="empty-state">No bash operators detected in these commands</p>'

    operators_html = ""
    # Sort by count descending
    sorted_ops = sorted(operators_used.items(), key=lambda x: -x[1])
    max_count = sorted_ops[0][1] if sorted_ops else 1

    for op, count in sorted_ops:
        name, desc = operator_descriptions.get(op, (op, 'Bash operator'))
        bar_width = (count / max_count) * 100
        operators_html += f'''
                                <div class="operator-item">
                                    <div class="operator-symbol"><code>{html.escape(op)}</code></div>
                                    <div class="operator-info">
                                        <div class="operator-name">{html.escape(name)}</div>
                                        <div class="operator-desc">{html.escape(desc)}</div>
                                    </div>
                                    <div class="operator-bar-container">
                                        <div class="operator-bar" style="width: {bar_width}%"></div>
                                    </div>
                                    <div class="operator-count">{count}</div>
                                </div>'''
    return operators_html


def render_overview_tab(stats: dict[str, Any], commands: list[dict], categories: dict) -> str:
    """Render the overview/dashboard tab content."""
    total_commands = stats.get("total_commands", 0)
    unique_commands = stats.get("unique_commands", 0)
    unique_utilities = stats.get("unique_utilities", 0)
    date_range = stats.get("date_range", {"start": "N/A", "end": "N/A"})

    # Get operators data for the "Bash Operators Used" section
    operators_used = stats.get("operators_used", {})
    operator_descriptions = {
        '|': ('Pipe', 'Sends output of one command to input of another'),
        '||': ('OR operator', 'Run next command if previous failed'),
        '&&': ('AND operator', 'Run next command if previous succeeded'),
        '2>&1': ('Redirect stderr', 'Combines error output with standard output'),
        '2>/dev/null': ('Suppress errors', 'Discards error messages'),
        '>': ('Redirect output', 'Writes output to a file (overwrites)'),
        '>>': ('Append output', 'Appends output to a file'),
        '<': ('Redirect input', 'Reads input from a file'),
    }

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
                            <h3>Bash Operators Used</h3>
                            <div class="operators-list">
                                {_generate_operators_html(operators_used, operator_descriptions)}
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

        # Flags breakdown with descriptions
        flags = cmd.get("flags", [])
        flags_html = ""
        if flags:
            flags_html = '<div class="flags-section"><h5>Flags:</h5><ul class="flags-list">'
            for flag in flags:
                flag_name = html.escape(flag.get("flag", ""))
                flag_desc = html.escape(flag.get("description", ""))
                if flag_desc:
                    flags_html += f'<li><code class="flag">{flag_name}</code> <span class="flag-desc">{flag_desc}</span></li>'
                else:
                    flags_html += f'<li><code class="flag">{flag_name}</code></li>'
            flags_html += '</ul></div>'

        # Subcommand description
        subcommand_desc = cmd.get("subcommand_desc", "")
        subcmd_html = ""
        if subcommand_desc:
            subcmd_html = f'<div class="subcmd-section"><span class="subcmd-label">Subcommand:</span> {html.escape(subcommand_desc)}</div>'

        # Common patterns / examples from knowledge base
        common_patterns = cmd.get("common_patterns", [])
        patterns_html = ""
        if common_patterns:
            patterns_html = '<div class="patterns-section"><h5>Common Patterns:</h5><ul class="patterns-list">'
            for pattern in common_patterns[:5]:
                patterns_html += f'<li><code>{html.escape(pattern)}</code></li>'
            patterns_html += '</ul></div>'

        # Output preview
        output_preview = cmd.get("output_preview", "")
        output_html = ""
        if output_preview:
            output_html = f'''
                            <div class="output-section">
                                <h5>Example Output:</h5>
                                <pre class="output-preview">{html.escape(output_preview)}</pre>
                            </div>'''

        # Use cases from knowledge base
        use_cases = cmd.get("use_cases", [])
        use_cases_html = ""
        if use_cases:
            use_cases_html = '<div class="use-cases-section"><h5>Use Cases:</h5><ul class="use-cases-list">'
            for uc in use_cases[:3]:
                use_cases_html += f'<li>{html.escape(uc)}</li>'
            use_cases_html += '</ul></div>'

        # Gotchas / pitfalls from knowledge base
        gotchas = cmd.get("gotchas", [])
        gotchas_html = ""
        if gotchas:
            gotchas_html = '<div class="gotchas-section"><h5>Common Pitfalls:</h5><ul class="gotchas-list">'
            for g in gotchas[:2]:
                gotchas_html += f'<li>{html.escape(g)}</li>'
            gotchas_html += '</ul></div>'

        # Related commands
        related = cmd.get("related", [])
        related_html = ""
        if related:
            related_chips = ' '.join(f'<code class="related-cmd">{html.escape(r)}</code>' for r in related[:5])
            related_html = f'<div class="related-section"><h5>Related:</h5> {related_chips}</div>'

        # Man page / documentation link
        man_url = cmd.get("man_url", "")
        man_link_html = ""
        if man_url:
            man_link_html = f'<a class="man-link" href="{html.escape(man_url)}" target="_blank" rel="noopener noreferrer" title="Documentation">docs</a>'

        commands_html += f'''
                        <div class="command-card" data-category="{category}" data-frequency="{frequency}" data-name="{base_cmd}">
                            <div class="command-header" onclick="toggleCommand('{cmd_id}')">
                                <div class="command-main">
                                    <code class="cmd">{base_cmd}</code>
                                    <span class="category-badge">{category}</span>
                                    {man_link_html}
                                </div>
                                <div class="command-meta">
                                    <span class="cmd-preview">{' '.join(description.split())[:60]}{'...' if len(' '.join(description.split())) > 60 else ''}</span>
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
                                {subcmd_html}
                                {flags_html}
                                {use_cases_html}
                                {gotchas_html}
                                {patterns_html}
                                {related_html}
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

            # Get flags and patterns for this command from COMMAND_DB
            cmd_flags = cmd.get("flags", [])
            lesson_flags_html = ""
            if cmd_flags:
                lesson_flags_html = '<div class="lesson-flags"><strong>Flags used:</strong> '
                flag_parts = []
                for flag in cmd_flags:
                    fname = html.escape(flag.get("flag", "") if isinstance(flag, dict) else str(flag))
                    fdesc = html.escape(flag.get("description", "") if isinstance(flag, dict) else "")
                    if fdesc:
                        flag_parts.append(f'<code class="flag">{fname}</code> ({fdesc})')
                    else:
                        flag_parts.append(f'<code class="flag">{fname}</code>')
                lesson_flags_html += ', '.join(flag_parts) + '</div>'

            # Subcommand info
            subcmd_desc = cmd.get("subcommand_desc", "")
            lesson_subcmd = ""
            if subcmd_desc:
                lesson_subcmd = f'<div class="lesson-subcmd"><em>{html.escape(subcmd_desc)}</em></div>'

            # Use cases and gotchas from COMMAND_DB for lessons
            lesson_use_cases = ""
            cmd_db_info = COMMAND_DB.get(base_cmd.replace("&amp;", "&"), {})
            uc_list = cmd_db_info.get("use_cases", [])
            if uc_list:
                uc_items = ''.join(f'<li>{html.escape(uc)}</li>' for uc in uc_list[:2])
                lesson_use_cases = f'<div class="lesson-use-cases"><strong>When to use:</strong><ul>{uc_items}</ul></div>'

            lesson_gotchas = ""
            gotcha_list = cmd_db_info.get("gotchas", [])
            if gotcha_list:
                g_items = ''.join(f'<li>{html.escape(g)}</li>' for g in gotcha_list[:1])
                lesson_gotchas = f'<div class="lesson-gotchas"><strong>Watch out:</strong><ul>{g_items}</ul></div>'

            lesson_man_url = ""
            man_link = cmd_db_info.get("man_url", "")
            if man_link:
                lesson_man_url = f'<a class="man-link" href="{html.escape(man_link)}" target="_blank" rel="noopener noreferrer">docs</a>'

            cat_commands_html += f'''
                            <div class="lesson-command">
                                <div class="lesson-command-header">
                                    <code class="cmd">{base_cmd}</code>
                                    <span class="lesson-complexity complexity-{complexity}">{complexity}</span>
                                    {lesson_man_url}
                                </div>
                                <pre class="syntax-highlighted">{highlighted}</pre>
                                <p class="lesson-description">{description}</p>
                                {lesson_subcmd}
                                {lesson_flags_html}
                                {lesson_use_cases}
                                {lesson_gotchas}
                            </div>'''

        # Patterns observed
        patterns = _extract_patterns(cat_cmd_data)
        patterns_html = ""
        if patterns:
            patterns_html = '<div class="patterns"><h4>Patterns Observed:</h4><ul>'
            for pattern in patterns:
                patterns_html += f'<li>{html.escape(pattern)}</li>'
            patterns_html += '</ul></div>'

        # Collect related commands across this category for cross-reference
        related_set = set()
        cat_base_cmds = {c.get("base_command", "") for c in cat_cmd_data}
        for cmd_item in cat_cmd_data:
            bc = cmd_item.get("base_command", "").replace("&amp;", "&")
            cmd_db_info = COMMAND_DB.get(bc, {})
            for rel in cmd_db_info.get("related", []):
                if rel not in cat_base_cmds:
                    related_set.add(rel)
        related_html = ""
        if related_set:
            related_chips = ' '.join(
                f'<code class="related-cmd">{html.escape(r)}</code>'
                for r in sorted(related_set)[:12]
            )
            related_html = f'<div class="lesson-related-section"><h4>Explore Related Commands:</h4><div class="related-chips">{related_chips}</div></div>'

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
                            {related_html}
                        </div>
                    </div>'''

    return f'''
                <div class="lessons-container">
                    {lessons_html}
                </div>'''


def _get_category_concept(category: str) -> str:
    """Get concept overview for a category."""
    concepts = {
        "File System": "Commands for navigating, viewing, creating, and managing files and directories in the filesystem.",
        "Text Processing": "Tools for viewing, searching, filtering, and transforming text content in files and streams.",
        "Git": "Version control system commands for tracking changes, managing branches, and collaborating on code.",
        "Package Management": "Package managers for installing, updating, and managing software dependencies across languages and platforms.",
        "Process & System": "Commands for monitoring, managing, and controlling running processes and system resources.",
        "Networking": "Commands for network operations, file transfers, remote access, and connectivity diagnostics.",
        "Permissions": "Commands for managing file ownership, access permissions, and user/group administration.",
        "Compression": "Commands for compressing, archiving, and extracting files using various algorithms.",
        "Search & Navigation": "Commands for finding files, searching content, and navigating the filesystem efficiently.",
        "Development": "Development tools for building, testing, compiling, and running code across languages.",
        "Shell Builtins": "Built-in shell commands for scripting, variable management, and interactive shell use.",
    }
    return concepts.get(category, f"Commands related to {category.lower()} operations and utilities.")


def _get_category_icon(category: str) -> str:
    """Get icon for a category."""
    icons = {
        "File System": "&#128193;",
        "Text Processing": "&#128196;",
        "Git": "&#128202;",
        "Package Management": "&#128230;",
        "Process & System": "&#9881;",
        "Networking": "&#127760;",
        "Permissions": "&#128274;",
        "Compression": "&#128230;",
        "Search & Navigation": "&#128269;",
        "Development": "&#128187;",
        "Shell Builtins": "&#10095;",
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
        q_man_url = quiz.get("man_url", "")

        # Doc link for quiz context
        q_meta_html = ""
        if q_man_url:
            q_meta_html = f'<div class="quiz-meta"><a class="man-link" href="{html.escape(q_man_url)}" target="_blank" rel="noopener noreferrer">docs</a></div>'

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
                        <div class="question-header">
                            <div class="question-number">Question {idx + 1}</div>
                            {q_meta_html}
                        </div>
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
        [data-theme="dark"] .gotchas-section,
        [data-theme="dark"] .lesson-gotchas { background: #3e2723; border-left-color: #ff8f00; }
        [data-theme="dark"] .gotchas-list li,
        [data-theme="dark"] .lesson-gotchas li { color: #ffcc80; }
        [data-theme="dark"] .gotchas-section h5,
        [data-theme="dark"] .lesson-gotchas strong { color: #ffb300; }
        [data-theme="dark"] .use-cases-list li,
        [data-theme="dark"] .lesson-use-cases li { color: #b0bec5; }
        [data-theme="dark"] .related-cmd { background: #1a237e; color: #90caf9; }
        [data-theme="dark"] .man-link { background: #0d47a1; color: #90caf9; }
        [data-theme="dark"] .subcmd-section { background: #0d253f; border-left-color: #4a9eff; }

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

        /* Operators List */
        .operators-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .operator-item {
            display: grid;
            grid-template-columns: 80px 1fr 120px 50px;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }

        .operator-item:last-child {
            border-bottom: none;
        }

        .operator-symbol {
            font-family: var(--font-mono);
            font-size: 1rem;
            font-weight: 600;
            color: var(--accent-primary);
        }

        .operator-symbol code {
            background: var(--bg-tertiary);
            padding: 4px 8px;
            border-radius: var(--radius-sm);
        }

        .operator-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .operator-name {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .operator-desc {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        .operator-bar-container {
            height: 20px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            overflow: hidden;
        }

        .operator-bar {
            height: 100%;
            background: var(--accent-primary);
            border-radius: var(--radius-sm);
            transition: width 0.5s ease;
        }

        .operator-count {
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

        .cmd-preview {
            font-size: 0.8rem;
            color: var(--text-secondary);
            max-width: 400px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
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

        .flag-desc { color: #6c757d; margin-left: 4px; }
        .flags-list li { margin: 4px 0; line-height: 1.5; }
        .subcmd-section { background: #f0f7ff; padding: 8px 12px; border-radius: 6px; margin: 8px 0; border-left: 3px solid #4a9eff; }
        .subcmd-label { font-weight: 600; color: #4a9eff; }
        .patterns-section { margin: 8px 0; }
        .patterns-section h5 { margin: 4px 0; color: #666; font-size: 0.85em; }
        .patterns-list { list-style: none; padding: 0; margin: 4px 0; }
        .patterns-list li { padding: 3px 0; }
        .patterns-list code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }
        .lesson-flags { margin: 6px 0; font-size: 0.9em; color: #555; }
        .lesson-subcmd { font-size: 0.9em; color: #4a9eff; margin: 4px 0; }
        .lesson-complexity { font-size: 0.75em; padding: 2px 8px; border-radius: 10px; margin-left: 8px; }
        .complexity-simple { background: #e8f5e9; color: #2e7d32; }
        .complexity-intermediate { background: #fff3e0; color: #e65100; }
        .complexity-advanced { background: #fce4ec; color: #c62828; }

        /* Enrichment: use cases */
        .use-cases-section, .lesson-use-cases { margin: 8px 0; }
        .use-cases-section h5, .lesson-use-cases strong { margin: 4px 0; color: #1a73e8; font-size: 0.85em; }
        .use-cases-list { padding-left: 18px; margin: 4px 0; }
        .use-cases-list li, .lesson-use-cases li { margin: 4px 0; line-height: 1.5; font-size: 0.9em; color: #444; }
        .lesson-use-cases ul { padding-left: 18px; margin: 4px 0; list-style: disc; }
        .lesson-use-cases li { font-size: 0.85em; color: #555; }

        /* Enrichment: gotchas / pitfalls */
        .gotchas-section, .lesson-gotchas { margin: 8px 0; background: #fff8e1; padding: 8px 12px; border-radius: 6px; border-left: 3px solid #f9a825; }
        .gotchas-section h5, .lesson-gotchas strong { margin: 4px 0; color: #f57f17; font-size: 0.85em; }
        .gotchas-list { padding-left: 18px; margin: 4px 0; }
        .gotchas-list li, .lesson-gotchas li { margin: 4px 0; line-height: 1.5; font-size: 0.9em; color: #5d4037; }
        .lesson-gotchas ul { padding-left: 18px; margin: 4px 0; list-style: disc; }

        /* Enrichment: related commands */
        .related-section { margin: 8px 0; }
        .related-section h5 { display: inline; margin-right: 6px; color: #666; font-size: 0.85em; }
        .related-cmd { background: #e8eaf6; color: #3949ab; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-right: 4px; cursor: default; }

        /* Enrichment: man page link */
        .man-link { font-size: 0.75em; padding: 2px 8px; border-radius: 10px; background: #e3f2fd; color: #1565c0; text-decoration: none; margin-left: 8px; font-weight: 500; }
        .man-link:hover { background: #bbdefb; text-decoration: none; }

        /* Quiz enrichment */
        .question-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .quiz-meta { display: flex; gap: 6px; align-items: center; }

        /* Lesson related commands */
        .lesson-related-section { margin: 16px 0 8px; padding: 12px; background: var(--bg-secondary); border-radius: var(--radius-md); border: 1px solid var(--border-color); }
        .lesson-related-section h4 { font-size: 0.9em; color: var(--text-secondary); margin-bottom: 8px; }
        .related-chips { display: flex; flex-wrap: wrap; gap: 6px; }

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

    # Build frequency map from top_commands (full command strings)
    top_commands_data = analysis.get('top_commands', [])
    frequency_map = {}
    for item in top_commands_data:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            cmd_str, count = item[0], item[1]
            frequency_map[cmd_str] = count

    # Get base command frequency for the "Top 10 Most-Used Commands" chart
    # This aggregates by base command (cd, git, mkdir) not full command strings
    top_base_commands_data = analysis.get('top_base_commands', [])

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
        cmd_str = cmd.get('command', '')
        base_cmd = cmd.get('base_command', cmd_str.split()[0] if cmd_str else '')
        complexity_score = cmd.get('complexity', 1)

        # Filter out non-bash entries (Python/JS code fragments, single chars, status text)
        if not base_cmd or len(base_cmd) < 2:
            continue
        # Skip entries that look like code fragments (contain parens, equals, dots as methods)
        if any(c in base_cmd for c in ('(', ')', '=', '{', '}')) and not base_cmd.startswith('.'):
            continue
        # Skip entries with backslashes, quotes, or HTML entities (JSONL text fragments)
        if any(c in base_cmd for c in ('\\', '"', "'")) or '&' in base_cmd:
            continue
        # Skip entries that are clearly not commands (capitalized status words, text fragments)
        if base_cmd[0].isupper() and base_cmd.isalpha() and base_cmd not in ('PATH', 'HOME'):
            continue
        # Skip common text fragments that get misidentified as commands
        junk_tokens = {'version', 'total', 'package', 'success', 'error', 'reading',
                       'editing', 'done', 'warning', 'info', 'note', 'output',
                       'task', 'goal', 'purpose', 'what', 'description'}
        if base_cmd.lower() in junk_tokens:
            continue

        # Tokenize the command for subcommand/description generation
        cmd_tokens = cmd_str.split() if cmd_str else []

        # Look up COMMAND_DB info for this command
        cmd_info = COMMAND_DB.get(base_cmd, {})
        kb_flags = get_flags_for_command(base_cmd)

        # Convert flags to expected format WITH descriptions from knowledge base
        # Filter out non-flag tokens: bare dashes, numeric args (-5, -30), trailing colons
        import re
        raw_flags = cmd.get('flags', [])
        formatted_flags = []
        seen_flags = set()
        for f in raw_flags:
            flag_name = f.get('flag', '') if isinstance(f, dict) else f
            # Skip bare dash, numeric-only flags (-5, -30), and artifact flags with colons
            if not flag_name or flag_name == '-' or flag_name.endswith(':'):
                continue
            if re.match(r'^-\d+$', flag_name):
                continue
            # Deduplicate flags within same command
            if flag_name in seen_flags:
                continue
            seen_flags.add(flag_name)

            if isinstance(f, dict) and 'flag' in f:
                flag_desc = f.get('description', '')
                if not flag_desc and flag_name in kb_flags:
                    flag_desc = kb_flags[flag_name]
                formatted_flags.append({'flag': flag_name, 'description': flag_desc})
            elif isinstance(f, str):
                flag_desc = kb_flags.get(f, '')
                # For combined flags like -la, decompose into individual flags
                if not flag_desc and len(f) > 2 and f.startswith('-') and not f.startswith('--'):
                    char_descs = []
                    for char in f[1:]:
                        single = f'-{char}'
                        if single in kb_flags:
                            char_descs.append(f'{single}: {kb_flags[single]}')
                    if char_descs:
                        flag_desc = '; '.join(char_descs)
                # For find-style flags (-name, -type, -path, -maxdepth), add descriptions
                if not flag_desc:
                    find_flags = {
                        '-name': 'Match files by name pattern',
                        '-type': 'Filter by file type (f=file, d=directory)',
                        '-path': 'Match files by path pattern',
                        '-maxdepth': 'Limit directory recursion depth',
                        '-mindepth': 'Set minimum directory depth',
                        '-exec': 'Execute command on each match',
                        '-not': 'Negate the following expression',
                        '-size': 'Match files by size',
                        '-mtime': 'Match by modification time',
                        '-perm': 'Match by file permissions',
                        '-ls': 'List matched files in ls -l format',
                        '-delete': 'Delete matched files',
                        '-print': 'Print matched file paths',
                    }
                    flag_desc = find_flags.get(f, '')
                # For common CLI flags without KB entries
                if not flag_desc:
                    common_flags = {
                        '--help': 'Show help and usage information',
                        '--version': 'Show version number',
                        '--verbose': 'Enable verbose output',
                        '--dry-run': 'Preview changes without executing',
                        '--output': 'Specify output file or directory',
                        '--open': 'Open result in default application',
                        '--stat': 'Show diffstat summary of changes',
                        '--sessions': 'Number of sessions to process',
                        '--title': 'Set custom title',
                        '--no-open': 'Skip auto-opening in browser',
                        '--from': 'Specify input source path',
                        '-s': 'Silent/short output mode',
                        '-n': 'Numeric/count or line number',
                        '-c': 'Execute command string or count',
                        '-g': 'Global scope',
                        '-p': 'Preserve attributes or port',
                        '-o': 'Output file',
                    }
                    flag_desc = common_flags.get(f, '')
                formatted_flags.append({'flag': f, 'description': flag_desc})

        # Generate a contextual description that differentiates commands with the same base
        session_desc = cmd.get('description', '')
        kb_desc = cmd_info.get('description', '')

        # Build a specific description from the actual command content
        args_list = cmd.get('args', [])
        flag_list = [fl.get('flag', '') if isinstance(fl, dict) else str(fl) for fl in formatted_flags]
        contextual_desc = ''

        # For inline code execution (python -c, bash -c), summarize the code snippet
        if base_cmd in ('python', 'python3', 'bash', 'sh', 'node') and '-c' in flag_list:
            # Extract the inline code from the full command after -c
            c_idx = cmd_str.find('-c')
            if c_idx >= 0:
                raw_code = cmd_str[c_idx + 2:].strip().strip('"').strip("'")
                # Split on actual newlines before collapsing
                code_lines = [l.strip() for l in raw_code.splitlines() if l.strip()]
                # Find first non-import line for a distinctive preview
                action_lines = [l for l in code_lines if not l.startswith(('import ', 'from ', '#'))]
                if action_lines:
                    code_part = ' '.join(action_lines[0].split())[:60]
                elif code_lines:
                    # All imports - show what's being imported
                    code_part = ' '.join(code_lines[0].split())[:60]
                else:
                    code_part = ''
                if code_part:
                    contextual_desc = f"{base_cmd} -c: {code_part}{'...' if len(code_part) >= 60 else ''}"

        # For commands with subcommands (git, npm, docker, etc.), use subcommand context
        if not contextual_desc and cmd_tokens and len(cmd_tokens) > 1:
            subcmd_token = next((t for t in cmd_tokens[1:] if not t.startswith('-') and not t.startswith('"') and not t.startswith("'")), '')
            if subcmd_token and subcmd_token != base_cmd:
                subcmd_info = cmd_info.get('subcommands', {}).get(subcmd_token, '')
                if subcmd_info:
                    contextual_desc = f"{base_cmd} {subcmd_token}: {subcmd_info}"
                else:
                    contextual_desc = f"{base_cmd} {subcmd_token}"
                # Add meaningful args (skip very long ones, quotes, code)
                short_args = [a for a in args_list if len(str(a)) < 40 and a != subcmd_token and not a.startswith('"')]
                if short_args:
                    contextual_desc += f" ({', '.join(short_args[:3])})"

        # For commands with flags but no subcommand, describe with flags
        if not contextual_desc and flag_list:
            flag_summary = ', '.join(flag_list[:3])
            short_args = [a for a in args_list if len(str(a)) < 40]
            if short_args:
                contextual_desc = f"{base_cmd} {flag_summary} on {', '.join(short_args[:2])}"
            else:
                contextual_desc = f"{base_cmd} with {flag_summary}"

        # For simple commands with just args
        if not contextual_desc and args_list:
            short_args = [a for a in args_list if len(str(a)) < 40]
            if short_args:
                contextual_desc = f"{base_cmd} {' '.join(short_args[:3])}"

        # Priority: contextual > knowledge base > generic fallback
        # Session descriptions (from JSONL) describe Claude's task, NOT the command
        if contextual_desc:
            description = contextual_desc
        elif kb_desc:
            description = kb_desc
        else:
            description = f"Run {base_cmd} command"

        # Get subcommand info (for commands like git, docker, npm)
        subcommands = cmd_info.get('subcommands', {})
        subcommand_desc = ''
        if subcommands and len(cmd_tokens) > 1:
            for token in cmd_tokens[1:]:
                if not token.startswith('-') and token in subcommands:
                    subcommand_desc = subcommands[token]
                    break

        # Get common patterns from COMMAND_DB
        common_patterns = cmd_info.get('common_patterns', [])

        formatted_commands.append({
            'base_command': base_cmd,
            'full_command': cmd_str,
            'category': cmd.get('category', 'Other'),
            'complexity': complexity_to_label(complexity_score),
            'complexity_score': complexity_score,
            'frequency': frequency_map.get(cmd_str, 1),
            'description': description,
            'flags': formatted_flags,
            'subcommand_desc': subcommand_desc,
            'common_patterns': common_patterns[:6],
            'args': cmd.get('args', []),
            'is_new': False,
            'man_url': cmd_info.get('man_url', ''),
            'use_cases': cmd_info.get('use_cases', []),
            'gotchas': cmd_info.get('gotchas', []),
            'related': cmd_info.get('related', []),
            'difficulty': cmd_info.get('difficulty', ''),
        })

    # Transform complexity distribution from numeric keys to string labels
    raw_complexity = stats.get('complexity_distribution', {})
    complexity_distribution = {
        'simple': raw_complexity.get(1, 0) + raw_complexity.get(2, 0),
        'intermediate': raw_complexity.get(3, 0),
        'advanced': raw_complexity.get(4, 0) + raw_complexity.get(5, 0),
    }

    # Build top commands list with proper frequencies (by base command)
    top_10_commands = []
    for item in top_base_commands_data[:10]:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            top_10_commands.append({
                'command': item[0],  # base command like "cd", "git"
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
            'operators_used': analysis.get('operators_used', {}),  # Bash operators like ||, &&, |, 2>&1
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

        # Extract base command from command_context for enrichment lookup
        cmd_ctx = quiz.get('command_context', '')
        base_cmd = cmd_ctx.split()[0] if cmd_ctx else ''
        q_cmd_info = COMMAND_DB.get(base_cmd, {})

        formatted_quizzes.append({
            'question': quiz.get('question', ''),
            'options': option_texts,
            'correct_answer': correct_idx,
            'explanation': quiz.get('explanation', ''),
            'difficulty': q_cmd_info.get('difficulty', ''),
            'man_url': q_cmd_info.get('man_url', ''),
            'base_command': base_cmd,
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
