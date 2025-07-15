#!/bin/bash

# gitt - Enhanced CLI that helps you write better commit messages with GUI option
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
    echo "  gitt              - Run CLI version"
    echo "  gitt --gui        - Run Streamlit GUI version"
    echo "  gitt --config-api - Configure Gemini API key"
    echo "  gitt --help       - Show this help message"
    exit 1
}

# Function to check if Python and required packages are available
check_gui_dependencies() {
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python3 is required for GUI mode"
        echo "Please install Python3 to use the GUI feature"
        exit 1
    fi
    
    # For GUI mode, prioritize the gitt config virtual environment
    # since that's where the GUI dependencies are installed
    if [ -f "$HOME/.config/gitt/.venv/bin/python" ]; then
        PYTHON_CMD="$HOME/.config/gitt/.venv/bin/python"
        echo "🐍 Using gitt virtual environment: $HOME/.config/gitt/.venv"
    elif [ -f ".venv/bin/python" ]; then
        PYTHON_CMD=".venv/bin/python"
        echo "🐍 Using local virtual environment: .venv"
        echo "⚠️  Note: GUI dependencies may not be available in local .venv"
    else
        PYTHON_CMD="python3"
        echo "🐍 Using system Python"
        echo "⚠️  Note: GUI dependencies may not be available in system Python"
    fi
    
    if ! $PYTHON_CMD -c "import streamlit" &> /dev/null; then
        echo "❌ Error: Streamlit is not installed in the selected Python environment"
        echo ""
        echo "To fix this issue:"
        if [ -f "$HOME/.config/gitt/.venv/bin/python" ]; then
            echo "1. Install dependencies in gitt config environment:"
            echo "   cd ~/.config/gitt && .venv/bin/pip install -r requirements.txt"
        else
            echo "1. Install dependencies in current environment:"
            echo "   $PYTHON_CMD -m pip install streamlit google-generativeai python-dotenv"
            echo "2. Or use the gitt config environment (recommended):"
            echo "   cd ~/.config/gitt && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
        fi
        echo ""
        exit 1
    fi
}

# Function to configure API key
configure_api_key() {
    echo "🔑 Gemini API Key Configuration"
    echo "================================"
    echo ""
    echo "To use AI-powered features, you need a Gemini API key."
    echo "Get your free API key from: https://makersuite.google.com/app/apikey"
    echo ""
    
    # Determine config directory
    CONFIG_DIR="$HOME/.config/gitt"
    ENV_FILE="$CONFIG_DIR/.env"
    
    # Create config directory if it doesn't exist
    mkdir -p "$CONFIG_DIR"
    
    # Check if .env already exists
    if [ -f "$ENV_FILE" ]; then
        echo "📄 Existing configuration found at: $ENV_FILE"
        if grep -q "GEMINI_API_KEY=" "$ENV_FILE" 2>/dev/null; then
            echo "✅ API key is already configured"
            echo ""
            read -p "Do you want to update it? [y/N]: " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "Configuration unchanged."
                return 0
            fi
        fi
    else
        # Create .env from template if it doesn't exist
        if [ -f "$CONFIG_DIR/.env.example" ]; then
            cp "$CONFIG_DIR/.env.example" "$ENV_FILE"
        fi
    fi
    
    echo ""
    echo "Enter your Gemini API key (it will be stored securely in $ENV_FILE):"
    read -r -s API_KEY
    echo ""
    
    if [ -z "$API_KEY" ]; then
        echo "❌ No API key provided. Configuration cancelled."
        return 1
    fi
    
    # Update or add the API key
    if [ -f "$ENV_FILE" ] && grep -q "GEMINI_API_KEY=" "$ENV_FILE"; then
        # Update existing key
        sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$API_KEY/" "$ENV_FILE"
    else
        # Add new key
        echo "GEMINI_API_KEY=$API_KEY" >> "$ENV_FILE"
    fi
    
    # Set secure permissions
    chmod 600 "$ENV_FILE"
    
    echo "✅ API key configured successfully!"
    echo "📁 Configuration saved to: $ENV_FILE"
    echo ""
    echo "You can now use AI features with:"
    echo "  gitt --gui    # GUI with AI commit messages"
    echo "  ~/.config/gitt/changelog_generator.py --since '1 week ago'  # AI changelogs"
}

# Function to launch GUI mode
launch_gui() {
    check_gui_dependencies
    
    echo "🚀 Launching Gitt GUI..."
    echo "📂 Current directory: $(pwd)"
    echo "Opening in your default web browser..."
    
    # Check if we're in a git repository first
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "⚠️  Warning: Not in a git repository"
        echo "The GUI will still launch, but git functionality will be limited"
    fi
    
    # Determine which GUI file to use and run with appropriate Python
    if [ -f "$HOME/.config/gitt/gitt_gui.py" ]; then
        echo "🎨 Using GUI from: $HOME/.config/gitt/"
        GUI_PATH="$HOME/.config/gitt/gitt_gui.py"
    elif [ -f "gitt_gui.py" ]; then
        echo "🎨 Using GUI from: $(pwd)"
        GUI_PATH="gitt_gui.py"
    else
        echo "❌ Error: gitt_gui.py not found"
        echo "Please ensure the GUI components are properly installed"
        echo "Expected locations:"
        echo "  - $HOME/.config/gitt/gitt_gui.py"
        echo "  - $(pwd)/gitt_gui.py"
        exit 1
    fi
    
    # Launch with the appropriate Python command
    echo "🚀 Starting Streamlit with: $PYTHON_CMD"
    $PYTHON_CMD -m streamlit run "$GUI_PATH" --server.port 8502 --server.headless true
}

# Function to run CLI mode (original functionality)
run_cli() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "Error: Not in a git repository"
        exit 1
    fi

    # Get the list of files to add
    GIT_FILES=$(git status --porcelain | awk '{print $2}')
    
    if [ -z "$GIT_FILES" ]; then
        echo "No changes detected in the repository."
        exit 0
    fi
    
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
    
    if [ $? -eq 0 ]; then
        echo "✅ Commit created successfully!"
    else
        echo "❌ Failed to create commit"
        exit 1
    fi
}

# Main script logic
case "${1:-}" in
    --gui)
        launch_gui
        ;;
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
