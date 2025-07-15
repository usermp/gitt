# Enhanced AI Commit Message Generation

## Overview
The Gitt GUI now features advanced AI-powered commit message generation that analyzes your git repository's changelog and context to create detailed, meaningful commit messages.

## Key Enhancements

### 1. File Change Analysis
- **File Type Detection**: Automatically identifies whether files are added, modified, deleted, or renamed
- **Change Summary**: Provides a structured overview of what changed in each file
- **Smart Grouping**: Groups related changes for cohesive commit messages

### 2. Git Statistics Integration
- **Line Count Analysis**: Tracks lines added/removed for each file
- **Impact Assessment**: Understands the scope of changes
- **File Statistics**: Provides quantitative context for the AI

### 3. Commit History Context
- **Recent Commits**: Analyzes last 5 commits for pattern consistency
- **Style Learning**: Maintains consistency with your project's commit style
- **Type Inference**: Better understands appropriate commit types based on history

### 4. Enhanced Diff Analysis
- **Deep Code Analysis**: Examines actual code changes, not just file names
- **Function-Level Changes**: Identifies specific functions/methods modified
- **Contextual Understanding**: Understands the purpose of changes

## Example Output

### Before (Simple AI):
```
Add GUI support
```

### After (Enhanced AI):
```
[feat] Add demo script and enhance gitt with GUI support

Introduced demo.sh to set up a test environment showcasing gitt features.

Enhanced gitt.sh to support a GUI mode using Streamlit and added API key configuration.

Created gitt_gui.py for the GUI interface, enabling AI-powered commit message generation.

Updated install.sh for cross-distro compatibility and improved installation process.

Added requirements.txt for Python dependencies needed for GUI functionality.
```

## New GitHelper Methods

### `get_file_changes_summary(files=None)`
Returns a dictionary mapping filenames to their change types and diffs.

### `get_file_stats(files=None)`
Returns git statistics showing lines added/removed for each file.

### `get_recent_commits_context(limit=5)`
Returns recent commit messages for style consistency.

### Enhanced `generate_commit_message(diff_content, commit_type=None, selected_files=None)`
Now accepts selected files and generates detailed, contextual commit messages.

## UI Improvements

1. **Expanded Text Area**: Larger commit message input (200px height)
2. **Message Statistics**: Shows title length, total lines, and body lines
3. **File Analysis View**: Optional panel showing what the AI analyzes
4. **Better Preview**: Enhanced commit message preview with formatting
5. **Smart Type Detection**: Avoids duplicate type prefixes

## Usage Tips

1. **Select Specific Files**: For best results, select specific files rather than "all changes"
2. **Review AI Output**: The AI generates comprehensive messages, but always review before committing
3. **Use File Analysis**: Check the "📊 Show File Analysis" option to see what context the AI uses
4. **Customize as Needed**: Edit the generated message to match your specific needs

## Configuration

The enhanced AI requires:
- Python package: `google-generativeai`
- Environment variable: `GEMINI_API_KEY`
- Git repository with changes to analyze

## Benefits

- **Consistency**: Maintains consistent commit message style across your project
- **Detail**: Provides comprehensive descriptions of changes
- **Context**: Understands the broader impact of changes
- **Time Saving**: Reduces time spent writing detailed commit messages
- **Quality**: Improves commit message quality with structured format
