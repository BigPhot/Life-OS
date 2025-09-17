#!/usr/bin/env python3
"""
Time tracking script for breakdown sub-steps
Usage: python track_step.py <breakdown_file> <step_id> <action>
Actions: start, complete, status, summary
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path


def load_breakdown(file_path):
    """Load breakdown JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Breakdown file '{file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{file_path}'")
        sys.exit(1)


def save_breakdown(file_path, data):
    """Save breakdown JSON file with proper formatting"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def find_step(data, step_id):
    """Find a step by ID in the breakdown data"""
    for i, step in enumerate(data['expanded_sub_steps']):
        if step['id'] == step_id:
            return i, step
    return None, None


def start_step(file_path, step_id):
    """Start timing a step"""
    data = load_breakdown(file_path)
    step_index, step = find_step(data, step_id)

    if step is None:
        print(f"Error: Step '{step_id}' not found in breakdown file")
        sys.exit(1)

    readable_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update step with start time
    data['expanded_sub_steps'][step_index].update({
        'start_time_iso': readable_time,
        'status': 'in_progress'
    })

    save_breakdown(file_path, data)
    print(f"✅ Timer started for {step_id} at {readable_time}")


def complete_step(file_path, step_id):
    """Complete a step and calculate duration"""
    data = load_breakdown(file_path)
    step_index, step = find_step(data, step_id)

    if step is None:
        print(f"Error: Step '{step_id}' not found in breakdown file")
        sys.exit(1)

    if 'start_time_iso' not in step:
        print(f"Warning: No start time found for {step_id}. Please run 'start' first.")
        sys.exit(1)

    # Calculate duration using stored start time
    start_time = datetime.fromisoformat(step['start_time_iso'].replace(' ', 'T'))
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    readable_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    duration_minutes = duration / 60

    # Update step with completion data
    data['expanded_sub_steps'][step_index].update({
        'end_time_iso': readable_end_time,
        'actual_duration_seconds': int(duration),
        'actual_duration_minutes': round(duration_minutes, 2),
        'status': 'completed'
    })

    save_breakdown(file_path, data)

    print(f"✅ Step {step_id} completed in {duration_minutes:.1f} minutes ({duration} seconds)")

    # Show comparison with estimate
    estimated = step.get('estimated_lines', 0)
    if estimated > 0:
        print(f"📊 Estimated: ~{estimated} lines of code")


def show_status(file_path, step_id):
    """Show status of a specific step"""
    data = load_breakdown(file_path)
    step_index, step = find_step(data, step_id)

    if step is None:
        print(f"❌ Step {step_id} not found in breakdown file")
        sys.exit(1)

    print(f"📋 Step Status for {step_id}:")
    print(f"  Title: {step.get('title', 'N/A')}")
    print(f"  Status: {step.get('status', 'pending')}")
    print(f"  Started: {step.get('start_time_iso', 'Not started')}")
    print(f"  Completed: {step.get('end_time_iso', 'Not completed')}")
    print(f"  Duration: {step.get('actual_duration_minutes', 'N/A')} minutes")
    print(f"  Estimated Lines: {step.get('estimated_lines', 'N/A')}")


def show_summary(file_path):
    """Show summary of all steps"""
    data = load_breakdown(file_path)
    steps = data['expanded_sub_steps']

    total_steps = len(steps)
    completed_steps = sum(1 for step in steps if step.get('status') == 'completed')
    in_progress_steps = sum(1 for step in steps if step.get('status') == 'in_progress')
    pending_steps = total_steps - completed_steps - in_progress_steps

    total_time = sum(step.get('actual_duration_minutes', 0) for step in steps)

    print("📊 Breakdown Summary:")
    print(f"  Total Steps: {total_steps}")
    print(f"  Completed: {completed_steps}")
    print(f"  In Progress: {in_progress_steps}")
    print(f"  Pending: {pending_steps}")
    print(f"  Total Time Spent: {total_time:.1f} minutes")

    if completed_steps > 0:
        completed_times = [step['actual_duration_minutes'] for step in steps
                          if step.get('actual_duration_minutes')]
        if completed_times:
            avg_time = sum(completed_times) / len(completed_times)
            print(f"  Average Time per Step: {avg_time:.1f} minutes")


def main():
    if len(sys.argv) < 3:
        print("Usage: python track_step.py <breakdown_file> <step_id> <action>")
        print("Actions: start, complete, status, summary")
        print("Example: python track_step.py SETUP_breakdown.json SETUP_001 start")
        print("For summary: python track_step.py SETUP_breakdown.json \"\" summary")
        sys.exit(1)

    breakdown_file = sys.argv[1]
    step_id = sys.argv[2] if len(sys.argv) > 2 else ""
    action = sys.argv[3] if len(sys.argv) > 3 else ""

    if not action:
        print("Error: Action is required")
        sys.exit(1)

    if not Path(breakdown_file).exists():
        print(f"Error: Breakdown file '{breakdown_file}' not found")
        sys.exit(1)

    if action == "start":
        if not step_id:
            print("Error: Step ID is required for 'start' action")
            sys.exit(1)
        start_step(breakdown_file, step_id)
    elif action == "complete":
        if not step_id:
            print("Error: Step ID is required for 'complete' action")
            sys.exit(1)
        complete_step(breakdown_file, step_id)
    elif action == "status":
        if not step_id:
            print("Error: Step ID is required for 'status' action")
            sys.exit(1)
        show_status(breakdown_file, step_id)
    elif action == "summary":
        show_summary(breakdown_file)
    else:
        print(f"Error: Invalid action '{action}'")
        print("Valid actions: start, complete, status, summary")
        sys.exit(1)


if __name__ == "__main__":
    main()