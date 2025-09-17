#!/bin/bash

# Calculate actual lines of code for a completed step
# Usage: ./lines.sh SETUP_001

STEP_ID="$1"

# Default to current breakdown if in Narrator-Console
BREAKDOWN_FILE=".ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json"

if [[ -z "$STEP_ID" ]]; then
    echo "Usage: $0 <step_id>"
    echo "Example: $0 SETUP_001"
    exit 1
fi

# Find the script relative to this file's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/calculate_actual_lines.py"

# Activate virtual environment and run Python script
cd "$PROJECT_ROOT"
source .venv/bin/activate

python "$PYTHON_SCRIPT" "$BREAKDOWN_FILE" "$STEP_ID"