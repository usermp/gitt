#!/bin/bash

# gitt - A CLI that helps you write better commit messages
# Author: Mohammad Yeganeh

declare -A COMMIT_TYPES=(
    ["feat"]="Feature"
    ["fix"]="Fix"
    ["chore"]="Chore"
    ["refactor"]="Refactor"
    ["docs"]="Documentation"
    ["style"]="Style"
    ["test"]="Test"
    ["perf"]="Performance"
    ["ci"]="Continuous Integration"
    ["build"]="Build"
    ["revert"]="Revert"
)

# Function to display usage information
usage() {
    echo "Usage:"
    echo "  gitt"
    exit 1
}

# Get the list of files to add
GIT_FILES=$(git status --porcelain | awk '{print $2}')
FILES=$( (echo "[ALL] Add all changes"; echo "$GIT_FILES") | fzf --height 40% --multi --ansi --preview "echo {}" --preview-window=up:1 )

# Check if the user selected files or pressed Ctrl+C
if [ -z "$FILES" ]; then
    echo "No files selected for adding."
    exit 1
fi

# Check if the user wants to add all files
if [[ "$FILES" == "[ALL] Add all changes" ]]; then
    git add .
else
    git add $FILES
fi

# Select commit type
COMMIT_TYPE=$(printf "%s\n" "${!COMMIT_TYPES[@]}" "none" "no type" | fzf --height 40% --ansi --preview "echo ${COMMIT_TYPES[{}]}" --preview-window=up:1)

if [ -z "$COMMIT_TYPE" ]; then
    echo "No commit type selected."
    exit 1
fi

# Prompt for commit message
read -p "Enter commit message: " COMMIT_MESSAGE

if [ -z "$COMMIT_MESSAGE" ]; then
    echo "Commit message is required."
    exit 1
fi

# Format and commit
if [[ "$COMMIT_TYPE" == "none" || "$COMMIT_TYPE" == "no type" ]]; then
    FINAL_COMMIT_MESSAGE="$COMMIT_MESSAGE"
else
    FINAL_COMMIT_MESSAGE="[$COMMIT_TYPE] $COMMIT_MESSAGE"
fi

git commit -m "$FINAL_COMMIT_MESSAGE"
