#!/bin/bash

# gitt - Enhanced CLI that helps you write better commit messages with CLI + AI
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

# Load environment variables
if [ -f "$HOME/.config/gitt/.env" ]; then
    export $(grep -v '^#' "$HOME/.config/gitt/.env" | xargs)
fi

usage() {
    echo "Usage:"
    echo "  gitt              - Run CLI version"
    echo "  gitt --gui        - Run Streamlit GUI version"
    echo "  gitt --config-api - Configure Cloudflare API key"
    echo "  gitt --help       - Show this help message"
    exit 1
}

configure_api_key() {
    CONFIG_DIR="$HOME/.config/gitt"
    ENV_FILE="$CONFIG_DIR/.env"

    mkdir -p "$CONFIG_DIR"

    echo "🔐 Configure Cloudflare AI Credentials"
    echo -n "Enter CLOUDFLARE_API_TOKEN: "
    read -r -s TOKEN
    echo
    echo -n "Enter CLOUDFLARE_ACCOUNT_ID: "
    read -r ACCOUNT
    echo

    echo "CLOUDFLARE_API_TOKEN=$TOKEN" > "$ENV_FILE"
    echo "CLOUDFLARE_ACCOUNT_ID=$ACCOUNT" >> "$ENV_FILE"

    chmod 600 "$ENV_FILE"
    echo "✅ Configuration saved to $ENV_FILE"
}

generate_commit_message_with_cloudflare() {
    local COMMIT_TYPE=$1
    local DIFF=$(git diff --cached)

    if [ -z "$DIFF" ]; then
        echo "⚠️ No staged changes. Please stage changes before generating commit message." >&2
        return 1
    fi

    JSON_PAYLOAD=$(jq -n --arg input "$DIFF" --arg type "$COMMIT_TYPE" '{
      "messages": [
        {
          "role": "system",
          "content": "You are a Git commit message generator. Given the git diff and commit type, output only a short, clear, imperative commit message (max 12 words). Use imperative verbs (e.g. Remove, Simplify, Update). Never include or repeat the commit type in the message. No punctuation. No explanations. Only the message content."
        },
        {
          "role": "user",
          "content": "Commit type: \($type)\n\nGit diff:\n\n\($input)"
        }
      ]
    }')

    local RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/meta/llama-3-8b-instruct" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$JSON_PAYLOAD")

    local RAW_MESSAGE=$(echo "$RESPONSE" | jq -r '.result.response')
    local COMMIT_MESSAGE=$(echo "$RAW_MESSAGE" | head -n 1)

    if [ -z "$COMMIT_MESSAGE" ] || [ "$COMMIT_MESSAGE" == "null" ]; then
        echo "❌ Failed to get commit message from Cloudflare AI" >&2
        return 1
    fi

    # echo
    # echo "💡 Suggested commit message:" >&2
    # echo "----------------------------------" >&2
    # echo "$COMMIT_MESSAGE" >&2
    # echo "----------------------------------" >&2

    # echo >&2
    # echo "📝 You can now edit the message (or press Enter to accept as-is):" >&2
    read -e -i "$COMMIT_MESSAGE" -p "> " EDITED_MESSAGE

    if [ -z "$EDITED_MESSAGE" ]; then
        EDITED_MESSAGE="$COMMIT_MESSAGE"
    fi

    echo "$EDITED_MESSAGE"
}


run_cli() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not inside a git repository."
        exit 1
    fi

    GIT_FILES=$(git status --porcelain | awk '{print $2}')
    if [ -z "$GIT_FILES" ]; then
        echo "📭 No changes to commit."
        exit 0
    fi

    FILES=$( (echo "[ALL] Add all changes"; echo "$GIT_FILES") | fzf --height 40% --multi --ansi)

    if [ -z "$FILES" ]; then
        echo "❌ No files selected."
        exit 1
    fi

    if [[ "$FILES" == "[ALL] Add all changes" ]]; then
        git add .
    else
        IFS=$'\n' read -rd '' -a FILE_ARRAY <<<"$FILES"
        git add "${FILE_ARRAY[@]}"
    fi

    COMMIT_TYPE=$(printf "%s\n" "${!COMMIT_TYPES[@]}" "none" "no type" | fzf --height 40% --ansi --preview "echo ${COMMIT_TYPES[{}]}" --preview-window=up:1)
    if [ -z "$COMMIT_TYPE" ]; then
        echo "❌ No commit type selected."
        exit 1
    fi

    read -p "Use AI to generate commit message? [Y/n]: " USE_AI
    if [[ "$USE_AI" =~ ^[Yy]$ || -z "$USE_AI" ]]; then
        COMMIT_MESSAGE=$(generate_commit_message_with_cloudflare "$COMMIT_TYPE")
    else
        read -p "Enter commit message: " COMMIT_MESSAGE
    fi

    if [ -z "$COMMIT_MESSAGE" ]; then
        echo "❌ Commit message is required."
        exit 1
    fi

    if [[ "$COMMIT_TYPE" == "none" || "$COMMIT_TYPE" == "no type" ]]; then
        FINAL_COMMIT_MESSAGE="$COMMIT_MESSAGE"
    else
        FINAL_COMMIT_MESSAGE="[$COMMIT_TYPE] $COMMIT_MESSAGE"
    fi

    echo
    echo "📝 Final commit message:"
    echo "$FINAL_COMMIT_MESSAGE"
    echo
    read -p "Confirm commit? [Y/n]: " CONFIRM_FINAL
    if [[ "$CONFIRM_FINAL" =~ ^[Nn]$ ]]; then
        echo "🚫 Commit aborted."
        exit 1
    fi

    git commit -m "$FINAL_COMMIT_MESSAGE"
    if [ $? -eq 0 ]; then
        echo "✅ Commit created successfully!"
    else
        echo "❌ Failed to create commit."
    fi
}

# Entry
case "${1:-}" in
    --config-api)
        configure_api_key
        ;;
    --help|-h)
        usage
        ;;
    "")
        run_cli
        ;;
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac
