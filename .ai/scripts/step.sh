#!/bin/bash

# Simplified wrapper for step tracking using Python
# Usage from project root:
#   ./step.sh start SETUP_001
#   ./step.sh complete SETUP_001
#   ./step.sh status SETUP_001
#   ./step.sh summary

STEP_ID="$1"
ACTION="$2"

# Default to current breakdown if in Narrator-Console
BREAKDOWN_FILE=".ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json"

# If first arg is an action, shift parameters
if [[ "$STEP_ID" =~ ^(start|complete|status|summary)$ ]]; then
    ACTION="$STEP_ID"
    STEP_ID="$2"
fi

# Find the script relative to this file's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/track_step.py"

# Activate virtual environment and run Python script
cd "$PROJECT_ROOT"
source .venv/bin/activate

if [[ "$ACTION" == "summary" ]]; then
    python "$PYTHON_SCRIPT" "$BREAKDOWN_FILE" "" "summary"
else
    python "$PYTHON_SCRIPT" "$BREAKDOWN_FILE" "$STEP_ID" "$ACTION"
fi