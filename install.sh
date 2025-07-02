#!/bin/bash

# install.sh - Script to install the gitt CLI
# Author: Mohammad Yeganeh

# Function to display usage information
usage() {
    echo "Usage: $0"
    exit 1
}

# Check for required dependencies
check_dependencies() {
    if ! command -v git &> /dev/null; then
        echo "git is not installed. Please install git and try again."
        exit 1
    fi

    if ! command -v fzf &> /dev/null; then
        echo "fzf is not installed. Please install fzf and try again."
        exit 1
    fi
}

# Install the script
install_script() {
    local TARGET_DIR="/usr/local/bin"
    sudo mkdir -p "$TARGET_DIR"
    sudo cp gitt.sh "$TARGET_DIR/gitt"
    sudo chmod +x "$TARGET_DIR/gitt"
    echo "gitt has been installed to $TARGET_DIR."
    echo "You can run it by typing 'gitt' in your terminal."
}

# Main script execution
check_dependencies
install_script
