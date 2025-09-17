# Step Time Tracking System

A system to track how long each breakdown sub-step takes to implement, automatically updating the breakdown JSON files with timing data.

## Setup

The system uses a Python virtual environment located at `/home/adhir/projects/Life-OS/.venv`.

## Usage

From the project root directory:

### Start timing a step
```bash
.ai/scripts/step.sh start SETUP_001
```

### Complete a step
```bash
.ai/scripts/step.sh complete SETUP_001
```

### Check step status
```bash
.ai/scripts/step.sh status SETUP_001
```

### View summary of all steps
```bash
.ai/scripts/step.sh summary
```

### Calculate actual lines of code
```bash
.ai/scripts/lines.sh SETUP_001
```

## What gets tracked

When you start a step, it adds:
- `start_time_iso`: Human-readable timestamp (YYYY-MM-DD HH:MM:SS)
- `status`: "in_progress"

When you complete a step, it adds:
- `end_time_iso`: Human-readable timestamp (YYYY-MM-DD HH:MM:SS)
- `actual_duration_seconds`: Total seconds taken
- `actual_duration_minutes`: Total minutes taken (rounded to 2 decimals)
- `status`: "completed"

When you calculate actual lines (separate command), it adds:
- `actual_lines`: Actual lines of code added (counts created files + estimates for modifications)

## Files

- `track_step.py`: Main Python script that handles JSON manipulation
- `step.sh`: Bash wrapper for easy usage
- `calculate_actual_lines.py`: Counts actual lines of code added for completed steps
- `lines.sh`: Bash wrapper for calculating actual lines

## Example Output

```
✅ Timer started for SETUP_001 at 2025-09-17 10:52:55
✅ Step SETUP_001 completed in 0.4 minutes (26 seconds)
📊 Estimated: ~45 lines of code
```

The timing data is automatically saved to the breakdown JSON file and can be used to improve future estimates.