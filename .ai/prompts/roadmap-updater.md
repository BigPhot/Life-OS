# Roadmap and Step Breakdown Updater

## Purpose
Update existing project roadmaps or step breakdown files while automatically preserving previous versions in a deprecated folder for historical reference.

## Usage
**Input Required:**
- Project name
- Current file path (roadmap or step breakdown)
- File type (roadmap or step_breakdown)
- Description of changes to make
- Version description for the deprecated file

## Prompt Template

```
You are a project file manager. I need you to update an existing roadmap or step breakdown file while preserving the previous version.

**Project Context:**
{PROJECT_NAME}

**Current File:**
{CURRENT_FILE_PATH}

**File Type:**
{FILE_TYPE} (roadmap or step_breakdown)

**Changes Requested:**
{CHANGE_DESCRIPTION}

**Version Description:**
{VERSION_DESCRIPTION} (e.g., "v3_pre_review_removal", "v4_after_setup_completion")

**Required Steps:**
1. **Backup Current Version:**
   - Read the current file
   - Create the deprecated folder if it doesn't exist: `{project_root}/.ai/tasks/{PROJECT_NAME}/roadmap/deprecated/`
   - Move current file to: `{project_root}/.ai/tasks/{PROJECT_NAME}/roadmap/deprecated/{VERSION_DESCRIPTION}.json`

2. **Apply Changes:**
   - Make the requested modifications to the file structure
   - Update version number in the JSON (if applicable)
   - Ensure all IDs, dependencies, and references remain consistent

3. **Validate Result:**
   - Verify the new file follows proper JSON structure
   - For roadmaps: Check that all dependencies reference valid step IDs
   - For step breakdowns: Check that all sub-step IDs follow proper naming convention
   - Ensure no broken references exist

4. **Save Updated File:**
   - Write the updated file back to the original file path
   - Confirm the deprecated version was saved successfully

**Change Types Supported:**

For Roadmaps:
- Remove/add steps
- Modify step descriptions or dependencies
- Reorder step sequence
- Update technical requirements
- Adjust time estimates
- Restructure step groupings

For Step Breakdowns:
- Remove/add sub-steps
- Modify sub-step descriptions or file actions
- Reorder sub-step sequence
- Update validation criteria
- Adjust time estimates
- Add/remove review sub-steps

**Output Requirements:**
- Confirm backup was created with timestamp
- Summarize changes made
- Provide new version number
- List any validation warnings or issues

Focus on maintaining roadmap integrity while preserving development history through versioning.
```

## Example Usage

**Example 1 - Roadmap Update:**
```
You are a project file manager. I need you to update an existing roadmap while preserving the previous version.

**Project Context:**
Narrator-Console

**Current File:**
/home/adhir/projects/Life-OS/.ai/tasks/Narrator-Console/roadmap/Narrator-Console_roadmap.json

**File Type:**
roadmap

**Changes Requested:**
Remove all standalone review steps (REVIEW_01, REVIEW_02, etc.) and update dependencies accordingly

**Version Description:**
v3_pre_review_removal

[Assistant would then execute the backup and update process...]
```

**Example 2 - Step Breakdown Update:**
```
You are a project file manager. I need you to update an existing step breakdown while preserving the previous version.

**Project Context:**
Narrator-Console

**Current File:**
/home/adhir/projects/Life-OS/.ai/tasks/Narrator-Console/roadmap/SETUP_breakdown.json

**File Type:**
step_breakdown

**Changes Requested:**
Add granular review sub-steps after every 2-3 implementation tasks and update the step to reflect current progress

**Version Description:**
v1_pre_review_integration

[Assistant would then execute the backup and update process...]
```

## Customization Notes

1. **Version Naming**: Adjust version naming convention based on your preferences
2. **Backup Location**: Modify deprecated folder structure if needed
3. **Validation Rules**: Add project-specific validation requirements
4. **Change Types**: Extend supported change types as needed

## Integration

This prompt works with:
- Task breakdown generators for creating new roadmaps
- Step breakdown generators for creating detailed sub-steps
- Time tracking systems for recording actual vs estimated times
- Project management workflows for milestone tracking
- Documentation generation for progress reports

Save this prompt and use it whenever you need to make roadmap or step breakdown modifications while preserving development history.