#!/bin/bash

# Session initialization script for Claude Code
# Automatically creates/updates session log when Claude window opens

DATE=$(date '+%Y-%m-%d %H:%M:%S')
SESSION_ID=$(date '+%Y%m%d_%H%M%S')
SESSION_FILE=".ai/claude/logs/session_${SESSION_ID}.md"
SESSION_INDEX=".ai/claude/logs/index.md"
SESSION_MARKER=".ai/claude/.current_session"

# Create directories if they don't exist
mkdir -p .ai/claude/logs

# Only create new session if this is actually a new session
if [ ! -f "$SESSION_MARKER" ] || [ "$(cat $SESSION_MARKER 2>/dev/null)" != "$SESSION_ID" ]; then
    echo "$SESSION_ID" > "$SESSION_MARKER"

    # Create new session file
    echo "# Session $SESSION_ID" > "$SESSION_FILE"
    echo "**Date:** $DATE" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    # Get current git status and recent commits
    echo "### Project State" >> "$SESSION_FILE"
    echo "\`\`\`" >> "$SESSION_FILE"
    echo "Branch: $(git branch --show-current 2>/dev/null || echo 'Not a git repo')" >> "$SESSION_FILE"
    echo "Status: $(git status --porcelain 2>/dev/null | wc -l) changed files" >> "$SESSION_FILE"
    echo "Last commit: $(git log -1 --oneline 2>/dev/null || echo 'No commits')" >> "$SESSION_FILE"
    echo "\`\`\`" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    # Check current setup progress from breakdown
    if [ -f ".ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json" ]; then
        echo "### Setup Progress" >> "$SESSION_FILE"
        COMPLETED=$(grep -o '"status": "completed"' .ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json | wc -l)
        TOTAL=$(grep -o '"id": "SETUP_[0-9]' .ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json | wc -l)
        echo "- Completed: $COMPLETED/$TOTAL setup steps" >> "$SESSION_FILE"
        echo "" >> "$SESSION_FILE"
    fi

    # Add session notes section
    echo "### Session Notes" >> "$SESSION_FILE"
    echo "- " >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    echo "### Commands Run" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    echo "### Decisions Made" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    echo "---" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"

    # Update session index
    if [ ! -f "$SESSION_INDEX" ]; then
        echo "# Session Index" > "$SESSION_INDEX"
        echo "" >> "$SESSION_INDEX"
        echo "## All Sessions" >> "$SESSION_INDEX"
        echo "" >> "$SESSION_INDEX"
    fi
    echo "- [$SESSION_ID - $DATE](session_${SESSION_ID}.md)" >> "$SESSION_INDEX"

    echo "New session created: $SESSION_FILE"
else
    echo "Continuing existing session: $(cat $SESSION_MARKER)"
fi

echo "Session initialized: $SESSION_ID"
echo ""
echo "🤖 REMINDER: Update the current session log as you work:"
echo "   - Add notes about what you're doing"
echo "   - Log important commands run"
echo "   - Record key decisions made"
echo "   - Track progress on current tasks"
echo ""