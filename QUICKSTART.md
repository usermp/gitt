# 🚀 Quick Start Guide

## 1️⃣ Installation

```bash
# Clone and install (works on all Linux distros)
git clone https://github.com/yourusername/gitt
cd gitt
chmod +x install.sh
./install.sh
```

**The installer automatically:**
- ✅ Detects your Linux distribution (Ubuntu, CentOS, Arch, etc.)
- ✅ Installs system dependencies (git, fzf, python3)
- ✅ Creates isolated virtual environment (.venv)
- ✅ Sets up CLI tool globally
- ✅ Installs GUI components

## 2️⃣ Setup API Key (Optional)

For AI features, get your Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Configure it:

```bash
# Global configuration (recommended)
cd ~/.config/gitt
cp .env.example .env
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Or project-specific
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

## 3️⃣ Basic Usage

### CLI Mode (Terminal)
```bash
gitt
```
- Use arrow keys and Enter to select files
- Choose files with space, Enter to confirm
- Select commit type from dropdown
- Enter commit message manually

### GUI Mode (Web Interface)
```bash
gitt --gui
```
- Opens in browser at http://localhost:8501
- Click checkboxes to select files
- Choose commit type from dropdown
- Use "🤖 Generate AI Commit Message" for smart suggestions
- Click "💾 Commit Changes"

## 4️⃣ Generate Changelog

```bash
# Recent changes
~/.config/gitt/changelog_generator.py --since "1 week ago"

# For specific version
~/.config/gitt/changelog_generator.py --version "v2.0.0" --since "v1.9.0"

# Without AI (basic format)
~/.config/gitt/changelog_generator.py --no-ai --since "1 month ago"
```

## 5️⃣ Try the Demo

```bash
# Creates test repository to try features
./demo.sh
cd /tmp/gitt_demo_*
gitt --gui
```

## 💡 Pro Tips

### **Cross-Platform Compatibility**
- Works on Ubuntu, Debian, CentOS, Fedora, Arch, openSUSE, Alpine
- Automatic dependency detection and installation
- Isolated Python environment prevents conflicts

### **AI Features**
- AI works best with meaningful file changes
- Shows context-aware commit suggestions
- Fallback to manual mode if API unavailable

### **GUI Benefits**
- Real-time diff preview
- Visual file selection with git status icons
- One-click commits with preview
- Works alongside CLI mode

### **Workflow Integration**
```bash
# Add to your shell aliases
alias gcm='gitt'           # Quick CLI access
alias gcm-gui='gitt --gui' # Quick GUI access

# VS Code integration
# Use terminal: gitt --gui (opens in browser)
```

## 🔧 Troubleshooting

### **Installation Issues**

**Missing dependencies:**
```bash
# The installer handles this automatically, but manually:
# Ubuntu/Debian:
sudo apt install git fzf python3 python3-pip python3-venv

# CentOS/Fedora:
sudo dnf install git fzf python3 python3-pip python3-venv

# Arch/Manjaro:
sudo pacman -S git fzf python python-pip
```

**Command not found:**
```bash
# Check if /usr/local/bin is in PATH
echo $PATH | grep /usr/local/bin

# If not, add to ~/.bashrc or ~/.zshrc:
export PATH="/usr/local/bin:$PATH"
source ~/.bashrc
```

### **GUI Issues**

**Streamlit not working:**
```bash
# Reinstall in virtual environment
cd ~/.config/gitt
.venv/bin/pip install --upgrade streamlit google-generativeai python-dotenv
```

**Port conflicts:**
```bash
# Kill existing processes
pkill -f streamlit

# Or use different port
~/.config/gitt/.venv/bin/streamlit run ~/.config/gitt/gitt_gui.py --server.port 8502
```

### **AI Issues**

**No AI suggestions:**
- Check your `.env` file has correct API key
- Verify internet connection
- Ensure API key has proper permissions
- Check API quota limits

**AI errors:**
```bash
# Test API key manually
cd ~/.config/gitt
source .env
~/.config/gitt/.venv/bin/python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
print('✅ API key works!')
"
```

### **Git Repository Issues**

**"Not in git repository":**
```bash
# Verify you're in a git repo
git status

# Initialize if needed
git init
```

## 🎯 Advanced Usage

### **Multiple Projects**
```bash
# Generate changelogs for multiple projects
for dir in project1 project2 project3; do
    cd "$dir" && ~/.config/gitt/changelog_generator.py --since "1 week ago"
done
```

### **Custom Commit Workflows**
```bash
# For conventional commits
gitt  # Select type + message = [type] message format

# Integration with hooks
# Add to .git/hooks/prepare-commit-msg for custom templates
```

### **Batch Operations**
```bash
# Quick commits across multiple files
gitt --gui  # Visual selection for complex changes
gitt        # CLI for simple, fast commits
```

## 🚀 What's Next?

1. **Explore commit types** - Learn when to use feat, fix, docs, etc.
2. **Try AI generation** - Let Gemini analyze your changes
3. **Generate changelogs** - Professional release notes automatically
4. **Customize workflow** - Integrate with your development process
5. **Contribute** - Help improve the tool for everyone!

Happy committing! 🎉

---

**Need help?** 
- 📖 Check the full [README](README.md)
- 🐛 Report issues on [GitHub](https://github.com/yourusername/gitt/issues)
- 💬 Join discussions for feature requests
