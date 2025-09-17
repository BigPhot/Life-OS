# Review Step GitHub Push Automation

## Purpose
Automatically commit and push changes to GitHub at review checkpoints with properly formatted commit messages that include step progress and validation status.

## Usage
**Input Required:**
- Project name
- Step ID that was just completed
- Review step ID (the next step)
- Brief description of what was implemented

## Prompt Template

```
You are a git automation assistant. I need you to create a commit and push to GitHub for a review checkpoint with a properly formatted commit message.

**Project Context:**
{PROJECT_NAME}

**Completed Step:**
{COMPLETED_STEP_ID} - {STEP_DESCRIPTION}

**Review Step:**
{REVIEW_STEP_ID}

**Implementation Summary:**
{IMPLEMENTATION_SUMMARY}

**Required Steps:**
1. **Check Git Status:**
   - Run `git status` to see all changes
   - Run `git diff` to review what will be committed

2. **Stage All Changes:**
   - Add all relevant files with `git add .`
   - Verify staged changes with `git status`

3. **Create Commit with Formatted Message:**
   - Use this commit message format:
   ```
   feat({PROJECT_NAME}): Complete {COMPLETED_STEP_ID} - {BRIEF_TITLE}

   Implemented:
   - {IMPLEMENTATION_POINT_1}
   - {IMPLEMENTATION_POINT_2}
   - {IMPLEMENTATION_POINT_3}

   Ready for {REVIEW_STEP_ID}: {REVIEW_DESCRIPTION}

   🤖 Generated with [Claude Code](https://claude.ai/code)


   ```

4. **Push to GitHub:**
   - Push the commit to the remote repository
   - Confirm the push was successful

5. **Provide Windows Testing Commands:**
   - Give a numbered list of exact command prompt commands to run
   - Include specific validation steps with expected outputs
   - Provide troubleshooting commands if needed

**Commit Message Guidelines:**
- Use conventional commit format (feat, fix, refactor, etc.)
- Include project name in scope
- Summarize what was implemented in bullet points
- Reference the next review step
- Keep the first line under 72 characters

**Output Requirements:**
- Confirm commit was created successfully
- Provide the commit SHA
- Give numbered Windows command prompt commands
- List expected outputs and validation criteria
- Provide troubleshooting commands if tests fail

Focus on creating clean, informative commit messages and providing exact Windows commands for manual testing.

**Windows Testing Command Format:**
```
## Windows Testing Commands

1. Open Command Prompt and navigate to project:
   ```cmd
   cd path\to\Life-OS
   git pull origin main
   ```

2. Install dependencies:
   ```cmd
   cd narrator-console
   npm install
   ```

3. Start the application:
   ```cmd
   npm run start
   ```

4. Validation checklist:
   - [ ] Electron window opens
   - [ ] Component renders correctly
   - [ ] No console errors
   - [ ] Feature X works as expected

5. Troubleshooting (if needed):
   ```cmd
   npm run lint
   npm run typecheck
   ```
```
```

## Example Usage

```
You are a git automation assistant. I need you to create a commit and push to GitHub for a review checkpoint.

**Project Context:**
Narrator-Console

**Completed Step:**
SETUP_004 - Configure Vite for Electron renderer process

**Review Step:**
SETUP_003_REVIEW - Validate basic Electron + React setup

**Implementation Summary:**
Created Vite configuration files for Electron main, renderer, and preload processes. Set up proper TypeScript compilation, HMR for development, and build targets for production.

[Assistant would then execute the git commands and create the formatted commit...]
```

## Customization Notes

1. **Commit Format**: Adjust the commit message template based on your preferences
2. **Branch Strategy**: Modify if you use feature branches instead of main
3. **Testing Instructions**: Customize Windows testing steps for your setup
4. **Validation Steps**: Add project-specific validation requirements

## Integration

This prompt works with:
- Step breakdown tracking for knowing what was completed
- Time tracking systems for including duration in commits
- Review step workflows for checkpoint validation
- Windows development environment for GUI testing

Use this prompt after completing any step that needs validation on Windows, especially GUI-related implementations.