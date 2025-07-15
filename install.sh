#!/bin/bash

# Enhanced installation script for gitt with GUI support and cross-distro compatibility

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# --- Update Mode ---

if [[ "$1" == "--update" ]]; then
    echo -e "${BLUE}🔄 Updating Gitt from local folder...${NC}"
    # Set update flag and re-run the script
    export GITT_UPDATE_MODE=1
    exec "$0"
fi

echo -e "${BLUE}🚀 Installing Gitt - Enhanced Git Commit Helper${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   exit 1
fi

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        OS=Debian
        VER=$(cat /etc/debian_version)
    elif [ -f /etc/SuSe-release ]; then
        OS=openSUSE
    elif [ -f /etc/redhat-release ]; then
        OS=RedHat
    else
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    echo -e "${BLUE}📋 Detected system: $OS $VER${NC}"
}

# Install dependencies based on distribution
install_dependencies() {
    echo -e "${BLUE}📦 Installing system dependencies...${NC}"
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*|*"Mint"*)
            sudo apt update
            if ! command -v git &> /dev/null; then
                sudo apt install -y git
            fi
            if ! command -v fzf &> /dev/null; then
                sudo apt install -y fzf
            fi
            if ! command -v python3 &> /dev/null; then
                sudo apt install -y python3 python3-pip python3-venv
            fi
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"Rocky"*|*"AlmaLinux"*)
            if command -v dnf &> /dev/null; then
                PKG_MGR="dnf"
            else
                PKG_MGR="yum"
            fi
            
            if ! command -v git &> /dev/null; then
                sudo $PKG_MGR install -y git
            fi
            if ! command -v fzf &> /dev/null; then
                sudo $PKG_MGR install -y fzf
            fi
            if ! command -v python3 &> /dev/null; then
                sudo $PKG_MGR install -y python3 python3-pip python3-venv
            fi
            ;;
        *"Arch"*|*"Manjaro"*)
            if ! command -v git &> /dev/null; then
                sudo pacman -S --noconfirm git
            fi
            if ! command -v fzf &> /dev/null; then
                sudo pacman -S --noconfirm fzf
            fi
            if ! command -v python3 &> /dev/null; then
                sudo pacman -S --noconfirm python python-pip
            fi
            ;;
        *"openSUSE"*|*"SLES"*)
            if ! command -v git &> /dev/null; then
                sudo zypper install -y git
            fi
            if ! command -v fzf &> /dev/null; then
                sudo zypper install -y fzf
            fi
            if ! command -v python3 &> /dev/null; then
                sudo zypper install -y python3 python3-pip python3-venv
            fi
            ;;
        *"Alpine"*)
            if ! command -v git &> /dev/null; then
                sudo apk add git
            fi
            if ! command -v fzf &> /dev/null; then
                sudo apk add fzf
            fi
            if ! command -v python3 &> /dev/null; then
                sudo apk add python3 py3-pip py3-virtualenv
            fi
            ;;
        *)
            echo -e "${YELLOW}⚠️  Unknown distribution. Please install git, fzf, and python3 manually.${NC}"
            ;;
    esac
}

# Check dependencies
echo -e "${BLUE}📋 Checking dependencies...${NC}"
detect_distro

# Check for git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git not found. Installing...${NC}"
    install_dependencies
else
    echo -e "${GREEN}✅ Git found${NC}"
fi

# Check for fzf
if ! command -v fzf &> /dev/null; then
    echo -e "${YELLOW}⚠️  fzf not found. Installing...${NC}"
    install_dependencies
else
    echo -e "${GREEN}✅ fzf found${NC}"
fi

# Check for python3
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 found${NC}"
    PYTHON_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  Python3 not found. Installing...${NC}"
    install_dependencies
    PYTHON_AVAILABLE=true
fi

echo

# Install the main script
echo -e "${BLUE}📦 Installing gitt...${NC}"

# Create installation directory if it doesn't exist
sudo mkdir -p /usr/local/bin

# Copy the main script only if source and destination differ
set +e  # Temporarily disable exit on error
if [ "$(realpath gitt.sh 2>/dev/null)" != "/usr/local/bin/gitt" ]; then
    if sudo cp gitt.sh /usr/local/bin/gitt 2>/dev/null; then
        sudo chmod +x /usr/local/bin/gitt
        echo -e "${GREEN}✅ gitt CLI installed to /usr/local/bin/gitt${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not copy gitt.sh. It may already be installed.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  gitt.sh is already at /usr/local/bin/gitt. Skipping copy.${NC}"
fi
set -e  # Re-enable exit on error

# Install GUI components if Python is available or if in update mode
if [ "$PYTHON_AVAILABLE" = true ] || [ "$GITT_UPDATE_MODE" = "1" ]; then
    echo -e "${BLUE}🎨 Setting up GUI components...${NC}"
    
    # Create gitt config directory
    GITT_DIR="$HOME/.config/gitt"
    mkdir -p "$GITT_DIR"
    
    # Copy GUI files (always update these during update mode)
    cp gitt_gui.py "$GITT_DIR/"
    cp requirements.txt "$GITT_DIR/"
    if [ -f .env.example ]; then
        cp .env.example "$GITT_DIR/"
    fi
    if [ -f changelog_generator.py ]; then
        cp changelog_generator.py "$GITT_DIR/"
    fi
    
    echo -e "${GREEN}✅ GUI components updated in $GITT_DIR${NC}"
    
    # Only create virtual environment if it doesn't exist
    if [ ! -d "$GITT_DIR/.venv" ]; then
        echo -e "${BLUE}🐍 Setting up Python virtual environment...${NC}"
        cd "$GITT_DIR"
        python3 -m venv .venv
    fi
    
    # Ask user if they want to install Python dependencies (skip in update mode if already installed)
    if [ "$GITT_UPDATE_MODE" = "1" ] && [ -f "$GITT_DIR/.venv/bin/pip" ]; then
        echo -e "${BLUE}📦 Updating Python dependencies...${NC}"
        cd "$GITT_DIR"
        .venv/bin/pip install --upgrade pip
        .venv/bin/pip install -r requirements.txt
        echo -e "${GREEN}✅ Python dependencies updated${NC}"
    elif [ "$GITT_UPDATE_MODE" != "1" ]; then
        echo
        read -p "$(echo -e ${BLUE}🐍 Install Python dependencies for GUI mode? [Y/n]: ${NC})" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo -e "${YELLOW}⚠️  Skipping Python dependencies. GUI mode will not work until installed.${NC}"
            echo -e "${YELLOW}   To install later: cd $GITT_DIR && .venv/bin/pip install -r requirements.txt${NC}"
        else
            echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
            cd "$GITT_DIR"
            .venv/bin/pip install --upgrade pip
            .venv/bin/pip install -r requirements.txt
            echo -e "${GREEN}✅ Python dependencies installed${NC}"
        fi
    fi
    
    # Setup API key (skip in update mode if .env already exists)
    if [ "$GITT_UPDATE_MODE" != "1" ] || [ ! -f "$GITT_DIR/.env" ]; then
        echo
        echo -e "${BLUE}🔑 Gemini API Setup${NC}"
        echo -e "${YELLOW}To use AI-powered commit messages, you need a Gemini API key.${NC}"
        echo -e "${YELLOW}1. Get your API key from: https://makersuite.google.com/app/apikey${NC}"
        echo -e "${YELLOW}2. Copy .env.example to .env in $GITT_DIR${NC}"
        echo -e "${YELLOW}3. Add your API key to the .env file${NC}"
        echo
        echo -e "${BLUE}Example:${NC}"
        echo -e "${YELLOW}cd $GITT_DIR${NC}"
        echo -e "${YELLOW}cp .env.example .env${NC}"
        echo -e "${YELLOW}echo 'GEMINI_API_KEY=your_actual_api_key_here' > .env${NC}"
    fi
fi

# Create a simple test to verify installation
echo
echo -e "${BLUE}🧪 Testing installation...${NC}"

if command -v gitt &> /dev/null; then
    echo -e "${GREEN}✅ gitt command is available${NC}"
    
    # Test if GUI components work
    if [ -f "$HOME/.config/gitt/gitt_gui.py" ] && [ -f "$HOME/.config/gitt/.venv/bin/python" ]; then
        if "$HOME/.config/gitt/.venv/bin/python" -c "import streamlit" &> /dev/null; then
            echo -e "${GREEN}✅ GUI components are ready${NC}"
        else
            echo -e "${YELLOW}⚠️  GUI dependencies need to be installed${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Installation failed${NC}"
    exit 1
fi

echo
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo
echo -e "${BLUE}Usage:${NC}"
echo -e "  ${GREEN}gitt${NC}        - Run CLI mode (requires fzf)"
if [ "$PYTHON_AVAILABLE" = true ]; then
    echo -e "  ${GREEN}gitt --gui${NC}  - Run GUI mode (requires Python dependencies)"
fi
echo -e "  ${GREEN}gitt --help${NC} - Show help"
echo

if [ "$PYTHON_AVAILABLE" = true ]; then
    echo -e "${YELLOW}💡 Don't forget to configure your Gemini API key for AI features!${NC}"
    echo -e "${YELLOW}   Configuration directory: $GITT_DIR${NC}"
fi

echo
echo -e "${BLUE}🚀 You can now use 'gitt' from anywhere in your terminal!${NC}"
