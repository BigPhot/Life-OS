# Infrastructure Step Breakdown Generator

## Purpose
Generate detailed, actionable sub-steps for infrastructure project steps, maintaining consistency across all breakdowns.

## Usage
**Input Required:**
- Project name/context
- Step ID from roadmap

## Prompt Template

```
You are an expert software infrastructure architect. I need you to create a detailed breakdown of implementation sub-steps for a specific step in my project roadmap.

**Project Context:**
{PROJECT_NAME}

**Technical Stack:**
- Framework: {FRAMEWORK}
- Language: {LANGUAGE}
- Build Tools: {BUILD_TOOLS}
- State Management: {STATE_MANAGEMENT}
- Styling: {STYLING_APPROACH}
- Additional Tools: {OTHER_TOOLS}

**Step to Break Down:**
- Step ID: {STEP_ID}
- Description: {STEP_DESCRIPTION}
- Dependencies: {DEPENDENCIES}
- Estimated Time: {ESTIMATED_TIME} minutes

**Current Sub-steps (high-level):**
{CURRENT_SUB_STEPS}

**Requirements:**
1. Expand each high-level sub-step into 2-4 granular, actionable tasks
2. Each granular task should represent 10-30 lines of code or a single focused operation
3. Include specific file names, component names, and technical decisions
4. Maintain logical sequence and dependencies between tasks
5. Consider error handling, testing, and validation at each step
6. Include configuration tasks (package.json updates, config files, etc.)
7. Specify which files to create vs modify
8. Include any necessary imports, exports, or interface definitions
9. Insert granular review/validation sub-steps after every 2-3 implementation tasks
10. Review sub-steps should verify functionality, test components, and validate current progress

**Output Format:**
Return a JSON structure with:
```json
{
  "step_id": "{STEP_ID}",
  "expanded_sub_steps": [
    {
      "id": "{STEP_ID}_001",
      "title": "Specific actionable task",
      "description": "Detailed description of what to implement",
      "file_actions": [
        "create: path/to/file.ts",
        "modify: existing/file.ts"
      ],
      "key_decisions": ["Technical choice 1", "Technical choice 2"],
      "estimated_lines": 25,
      "validation": "How to verify this step is complete"
    },
    {
      "id": "{STEP_ID}_002",
      "title": "Review: Validate previous implementation",
      "description": "Test and verify the functionality implemented in previous sub-steps",
      "file_actions": [
        "test: run specific commands or checks"
      ],
      "key_decisions": ["Validation approach", "Error handling strategy"],
      "estimated_lines": 0,
      "validation": "All previous tasks are working correctly"
    }
  ],
  "total_tasks": 12,
  "dependencies_resolved": ["Confirm dependency X is ready"],
  "potential_blockers": ["Issue that might arise"],
  "success_criteria": ["Step is complete when..."]
}
```

**File Output Requirement:**
Save the output JSON as a file in the same repository as the roadmap you generated it from, using the path pattern:
`{project_root}/.ai/tasks/{PROJECT_NAME}/roadmap/{STEP_ID}_breakdown.json`

Focus on infrastructure-quality code: robust error handling, proper TypeScript typing, modular architecture, and maintainable patterns.
```

## Example Usage

For Step ID "SETUP" from Narrator-Console project:

```
You are an expert software infrastructure architect. I need you to create a detailed breakdown of implementation sub-steps for a specific step in my project roadmap.

**Project Context:**
Narrator-Console - A desktop application for life tracking and visualization

**Technical Stack:**
- Framework: Electron + React + TypeScript
- Language: TypeScript
- Build Tools: Vite + Electron Forge
- State Management: Redux Toolkit
- Styling: Tailwind CSS
- Additional Tools: ESLint, Prettier

**Step to Break Down:**
- Step ID: SETUP
- Description: Project initialization and configuration
- Dependencies: []
- Estimated Time: 60 minutes

**Current Sub-steps (high-level):**
- Initialize Electron project structure
- Set up React with TypeScript
- Configure Vite build system
- Install Tailwind CSS and configure
- Set up Redux Toolkit store
- Configure Electron main/renderer process communication
- Create folder structure for components/pages/services
- Set up React Router for navigation
- Configure ESLint and Prettier
- Create development vs production configs

[Rest of prompt...]
```

## Customization Notes

1. **Technical Stack**: Update the technical stack section based on your project
2. **Output Format**: Modify the JSON structure if you need different fields
3. **Validation**: Adjust validation requirements based on your testing approach
4. **File Structure**: Customize file naming conventions and folder structure patterns

## Integration

This prompt can be used with:
- Claude Code for immediate implementation
- Other AI assistants for planning
- Project management tools for task creation
- Documentation generation workflows

Save this prompt and customize the placeholders for each project step breakdown.