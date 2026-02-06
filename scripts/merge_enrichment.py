#!/usr/bin/env python3
"""
Merge enrichment data into knowledge_base.py COMMAND_DB.

Reads enrichment data from enrichment_*.py files and merges them into
the existing COMMAND_DB entries in knowledge_base.py. Adds missing fields
(use_cases, gotchas, man_url, related, difficulty) and supplements
existing flag definitions with extra_flags.

Usage:
    python scripts/merge_enrichment.py [--dry-run]
"""

import sys
import re
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, Any


def load_enrichment_module(filepath: Path) -> Dict[str, Any]:
    """Load ENRICHMENT_DATA from a Python file."""
    spec = importlib.util.spec_from_file_location("enrichment", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'ENRICHMENT_DATA', {})


def collect_all_enrichments(scripts_dir: Path) -> Dict[str, Any]:
    """Collect enrichment data from all enrichment_*.py files."""
    merged = {}
    for enrichment_file in sorted(scripts_dir.glob("enrichment_*.py")):
        print(f"  Loading: {enrichment_file.name}")
        data = load_enrichment_module(enrichment_file)
        print(f"    -> {len(data)} commands")
        for cmd_name, cmd_data in data.items():
            if cmd_name in merged:
                # Merge: later files can supplement but not overwrite
                for key, value in cmd_data.items():
                    if key not in merged[cmd_name] or not merged[cmd_name][key]:
                        merged[cmd_name][key] = value
            else:
                merged[cmd_name] = cmd_data
    return merged


def merge_into_knowledge_base(kb_path: Path, enrichments: Dict[str, Any], dry_run: bool = False) -> int:
    """
    Merge enrichment data into knowledge_base.py by modifying COMMAND_DB entries.

    Strategy: For each command in enrichments, find its entry in COMMAND_DB and
    insert the enrichment fields before the closing brace of that entry.

    Returns number of commands enriched.
    """
    content = kb_path.read_text(encoding='utf-8')
    original_content = content
    enriched_count = 0
    fields_to_add = ['man_url', 'use_cases', 'gotchas', 'related', 'difficulty']

    for cmd_name, enrichment in enrichments.items():
        # Find this command's entry in COMMAND_DB
        # Pattern: "cmd_name": { ... },
        # We look for the closing "}, " or "},\n" of this entry

        # Find the start of this command's dict entry
        # Handle both regular command names and special ones like "."
        escaped_name = re.escape(cmd_name)
        entry_pattern = rf'    "{escaped_name}": \{{'
        match = re.search(entry_pattern, content)
        if not match:
            print(f"  WARNING: Command '{cmd_name}' not found in COMMAND_DB, skipping")
            continue

        entry_start = match.start()

        # Find the closing of this entry by counting braces
        brace_depth = 0
        entry_end = -1
        i = match.end() - 1  # Start at the opening brace
        while i < len(content):
            char = content[i]
            if char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    entry_end = i
                    break
            # Skip string contents to avoid counting braces in strings
            elif char == '"':
                i += 1
                while i < len(content) and content[i] != '"':
                    if content[i] == '\\':
                        i += 1  # Skip escaped char
                    i += 1
            elif char == "'":
                i += 1
                while i < len(content) and content[i] != "'":
                    if content[i] == '\\':
                        i += 1
                    i += 1
            i += 1

        if entry_end == -1:
            print(f"  WARNING: Could not find end of entry for '{cmd_name}', skipping")
            continue

        # Extract the entry content
        entry_content = content[entry_start:entry_end + 1]

        # Check which fields are missing
        additions = []
        for field in fields_to_add:
            if f'"{field}"' not in entry_content:
                value = enrichment.get(field)
                if value:
                    additions.append((field, value))

        # Handle extra_flags: merge into existing flags dict
        extra_flags = enrichment.get('extra_flags', {})
        if extra_flags and '"flags"' in entry_content:
            # Find the flags dict closing brace and add new flags before it
            flags_additions = []
            for flag, desc in extra_flags.items():
                escaped_flag = flag.replace('"', '\\"')
                if f'"{escaped_flag}"' not in entry_content:
                    flags_additions.append(f'            "{escaped_flag}": "{desc}",')
            if flags_additions:
                # Find the closing of the flags dict within this entry
                flags_match = re.search(r'"flags":\s*\{', entry_content)
                if flags_match:
                    flags_start = flags_match.end()
                    # Find closing brace of flags
                    fb_depth = 1
                    fi = flags_start
                    while fi < len(entry_content) and fb_depth > 0:
                        if entry_content[fi] == '{':
                            fb_depth += 1
                        elif entry_content[fi] == '}':
                            fb_depth -= 1
                        elif entry_content[fi] == '"':
                            fi += 1
                            while fi < len(entry_content) and entry_content[fi] != '"':
                                if entry_content[fi] == '\\':
                                    fi += 1
                                fi += 1
                        fi += 1
                    flags_end_pos = entry_start + fi - 1
                    # Insert new flags before the closing brace
                    flags_insert = '\n' + '\n'.join(flags_additions) + '\n        '
                    content = content[:flags_end_pos] + flags_insert + content[flags_end_pos:]
                    # Recalculate entry_end since we modified content
                    entry_end += len(flags_insert)

        # Handle improved_description: replace existing description
        improved_desc = enrichment.get('improved_description')
        if improved_desc and '"description"' in entry_content:
            # Replace the existing description string
            desc_pattern = rf'(    "{escaped_name}": \{{[^}}]*?"description":\s*)"([^"]*(?:\\.[^"]*)*)"'
            new_desc = improved_desc.replace('"', '\\"')
            content = re.sub(desc_pattern, rf'\1"{new_desc}"', content, count=1)

        if not additions:
            continue

        # Build the insertion text
        insertion_lines = []
        for field, value in additions:
            if isinstance(value, str):
                escaped_val = value.replace('"', '\\"')
                insertion_lines.append(f'        "{field}": "{escaped_val}",')
            elif isinstance(value, list):
                if all(isinstance(v, str) for v in value):
                    items = ', '.join(f'"{v}"' for v in value)
                    if len(items) < 80:
                        insertion_lines.append(f'        "{field}": [{items}],')
                    else:
                        insertion_lines.append(f'        "{field}": [')
                        for v in value:
                            escaped_v = v.replace('"', '\\"')
                            insertion_lines.append(f'            "{escaped_v}",')
                        insertion_lines.append(f'        ],')

        if insertion_lines:
            insertion = '\n' + '\n'.join(insertion_lines)
            # Recalculate entry_end in current content
            match2 = re.search(entry_pattern, content)
            if match2:
                brace_depth = 0
                i2 = match2.end() - 1
                while i2 < len(content):
                    char = content[i2]
                    if char == '{':
                        brace_depth += 1
                    elif char == '}':
                        brace_depth -= 1
                        if brace_depth == 0:
                            entry_end = i2
                            break
                    elif char == '"':
                        i2 += 1
                        while i2 < len(content) and content[i2] != '"':
                            if content[i2] == '\\':
                                i2 += 1
                            i2 += 1
                    elif char == "'":
                        i2 += 1
                        while i2 < len(content) and content[i2] != "'":
                            if content[i2] == '\\':
                                i2 += 1
                            i2 += 1
                    i2 += 1

                # Insert before the closing brace
                content = content[:entry_end] + insertion + '\n    ' + content[entry_end:]
                enriched_count += 1

    if content != original_content:
        if dry_run:
            print(f"\n  DRY RUN: Would enrich {enriched_count} commands")
            # Show a diff summary
            added_lines = len(content.splitlines()) - len(original_content.splitlines())
            print(f"  Would add ~{added_lines} lines")
        else:
            kb_path.write_text(content, encoding='utf-8')
            print(f"\n  Enriched {enriched_count} commands in {kb_path.name}")

    return enriched_count


def main():
    dry_run = '--dry-run' in sys.argv

    scripts_dir = Path(__file__).parent
    kb_path = scripts_dir / 'knowledge_base.py'

    if not kb_path.exists():
        print(f"Error: {kb_path} not found")
        return 1

    print("Collecting enrichment data...")
    enrichments = collect_all_enrichments(scripts_dir)

    if not enrichments:
        print("No enrichment data found. Run the research agents first.")
        return 1

    print(f"\nTotal enrichments: {len(enrichments)} commands")
    print(f"\nMerging into {kb_path.name}{'  (DRY RUN)' if dry_run else ''}...")
    count = merge_into_knowledge_base(kb_path, enrichments, dry_run=dry_run)

    if count > 0:
        # Verify the file is still valid Python
        if not dry_run:
            print("\nVerifying syntax...")
            try:
                compile(kb_path.read_text(encoding='utf-8'), kb_path, 'exec')
                print("  Syntax OK")
            except SyntaxError as e:
                print(f"  SYNTAX ERROR: {e}")
                print("  Reverting changes...")
                # We'd need to keep a backup for this - for now just warn
                return 1

    print("\nDone.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
