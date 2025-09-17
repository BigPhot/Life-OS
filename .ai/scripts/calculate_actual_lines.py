#!/usr/bin/env python3
"""
Calculate actual lines of code added for a completed step and update the breakdown JSON.
Usage: python calculate_actual_lines.py <breakdown_file> <step_id>
"""

import json
import sys
import os
from pathlib import Path


def count_lines_in_file(file_path):
    """Count non-empty, non-comment lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Count non-empty lines that aren't just comments or whitespace
        actual_lines = 0
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and stripped != '*/':
                actual_lines += 1

        return actual_lines
    except (FileNotFoundError, UnicodeDecodeError):
        return 0


def calculate_actual_lines(breakdown_file, step_id):
    """Calculate actual lines added for a step based on its file_actions"""

    # Load breakdown JSON
    try:
        with open(breakdown_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading breakdown file: {e}")
        return False

    # Find the step
    step_found = False
    step_index = None
    for i, step in enumerate(data['expanded_sub_steps']):
        if step['id'] == step_id:
            step_found = True
            step_index = i
            break

    if not step_found:
        print(f"Step {step_id} not found in breakdown file")
        return False

    step = data['expanded_sub_steps'][step_index]

    # Check if step is completed
    if step.get('status') != 'completed':
        print(f"Step {step_id} is not completed yet")
        return False

    # Check if actual_lines already exists
    if 'actual_lines' in step:
        print(f"Step {step_id} already has actual_lines: {step['actual_lines']}")
        return True

    # Calculate actual lines from file_actions
    total_lines = 0
    file_actions = step.get('file_actions', [])

    # Get the project root (assume narrator-console directory)
    # The breakdown file is at .ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json
    # The project root should be at the same level as .ai
    breakdown_path = Path(breakdown_file)
    if breakdown_path.is_absolute():
        # Find the .ai directory and go up from there
        ai_index = None
        for i, part in enumerate(breakdown_path.parts):
            if part == '.ai':
                ai_index = i
                break
        if ai_index is not None:
            project_root = Path('/'.join(breakdown_path.parts[:ai_index])) / 'narrator-console'
        else:
            project_root = Path.cwd() / 'narrator-console'
    else:
        project_root = Path.cwd() / 'narrator-console'

    project_root = project_root.resolve()

    print(f"Looking for files in: {project_root}")

    for action in file_actions:
        if action.startswith('create:'):
            # Extract file path
            file_path = action.split('create:', 1)[1].strip()
            full_path = project_root / file_path

            lines = count_lines_in_file(full_path)
            if lines > 0:
                print(f"  {file_path}: {lines} lines")
                total_lines += lines
        elif action.startswith('modify:'):
            # For modifications, we'll estimate based on typical changes
            # This is approximate since we don't track exact changes
            file_path = action.split('modify:', 1)[1].strip()
            print(f"  {file_path}: ~5 lines (estimated for modification)")
            total_lines += 5  # Rough estimate for modifications

    # Update the step with actual_lines
    data['expanded_sub_steps'][step_index]['actual_lines'] = total_lines

    # Save updated breakdown
    with open(breakdown_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Updated {step_id} with actual_lines: {total_lines}")
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python calculate_actual_lines.py <breakdown_file> <step_id>")
        print("Example: python calculate_actual_lines.py SETUP_breakdown.json SETUP_001")
        sys.exit(1)

    breakdown_file = sys.argv[1]
    step_id = sys.argv[2]

    # Make breakdown_file path absolute if it's relative
    if not os.path.isabs(breakdown_file):
        # Check if it's already a full relative path
        if not breakdown_file.startswith('.ai/'):
            breakdown_file = f".ai/tasks/Narrator-Console/roadmap/{breakdown_file}"

    success = calculate_actual_lines(breakdown_file, step_id)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()