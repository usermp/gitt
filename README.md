# 🚀 Gitt - Enhanced Git Commit Helper with AI

> A powerful, cross-platform CLI and GUI tool that helps you write better commit messages with AI-powered suggestions and automated changelog generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://www.linux.org/)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

### 🎯 **Dual Interface**
- **CLI Mode**: Fast terminal-based interface with `fzf` integration
- **GUI Mode**: Beautiful web-based Streamlit interface

### 🤖 **AI-Powered**
- Generate intelligent commit messages using **Gemini 1.5 Flash**
- Context-aware suggestions based on your code changes
- Supports all major commit types and conventions

### 📝 **Smart Changelog Generation**
- Automatic changelog creation from git history
- Professional formatting with AI enhancement
- Version-based organization and categorization

### 🔧 **Cross-Platform Compatibility**
- **Universal Linux Support**: Ubuntu, Debian, CentOS, Fedora, Arch, openSUSE, Alpine
- **Automatic Dependency Management**: Detects and installs required packages
- **Virtual Environment**: Isolated Python dependencies with `.venv`

### 🎨 **Modern Features**
- Real-time diff preview
- Visual file selection with git status indicators
- One-click commit execution
- Professional commit type categorization

## � Installation

### 🚀 **Quick Install (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/gitt.git
cd gitt

# Make installer executable and run
chmod +x install.sh
./install.sh
```

The installer automatically:
- ✅ Detects your Linux distribution
- ✅ Installs system dependencies (git, fzf, python3)
- ✅ Sets up the CLI tool globally
- ✅ Creates isolated Python virtual environment
- ✅ Installs GUI components
- ✅ Configures AI features

### 🔧 **Manual Installation**

<details>
<summary>Click to expand manual installation steps</summary>

#### Prerequisites
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y git fzf python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install -y git fzf python3 python3-pip python3-venv

# Arch/Manjaro
sudo pacman -S git fzf python python-pip

# openSUSE
sudo zypper install git fzf python3 python3-pip python3-venv
```

#### Install Steps
```bash
# 1. Install CLI
sudo cp gitt.sh /usr/local/bin/gitt
sudo chmod +x /usr/local/bin/gitt

# 2. Setup GUI (optional)
mkdir -p ~/.config/gitt
cp gitt_gui.py requirements.txt .env.example changelog_generator.py ~/.config/gitt/

# 3. Create virtual environment
cd ~/.config/gitt
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

</details>

## 🎯 Usage

### 💻 **CLI Mode (Terminal)**
```bash
gitt
```
- Interactive file selection with `fzf`
- Commit type dropdown
- Manual message input
- Instant commit execution

### 🎨 **GUI Mode (Web Interface)**
```bash
gitt --gui
```
- Opens at `http://localhost:8501`
- Visual file selection with status icons
- AI-powered commit message generation
- Real-time diff preview
- One-click commits

### 📊 **Generate Changelog**
```bash
# Recent commits
~/.config/gitt/changelog_generator.py --since "1 week ago"

# Specific version
~/.config/gitt/changelog_generator.py --version "v2.0.0" --since "v1.9.0"

# Basic mode (no AI)
~/.config/gitt/changelog_generator.py --no-ai --since "1 month ago"
```

### ❓ **Help**
```bash
gitt --help
```

## 🔑 AI Configuration

### **Get Gemini API Key**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Configure in your environment:

```bash
# Method 1: Global configuration
cd ~/.config/gitt
cp .env.example .env
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Method 2: Project-specific
# Create .env in your project root with:
GEMINI_API_KEY=your_actual_api_key_here
```

## �️ Commit Types

| Type | Description | Icon | Example |
|------|------------|------|---------|
| **feat** | New feature | ✨ | `[feat] Add user authentication` |
| **fix** | Bug fix | 🐛 | `[fix] Resolve login timeout issue` |
| **docs** | Documentation | 📝 | `[docs] Update API documentation` |
| **style** | Code formatting | 💄 | `[style] Fix indentation in main.py` |
| **refactor** | Code restructuring | ♻️ | `[refactor] Simplify user service` |
| **test** | Testing | ✅ | `[test] Add unit tests for utils` |
| **chore** | Maintenance | 🔧 | `[chore] Update dependencies` |
| **perf** | Performance | ⚡ | `[perf] Optimize database queries` |
| **ci** | CI/CD | 👷 | `[ci] Add GitHub Actions workflow` |
| **build** | Build system | 📦 | `[build] Update webpack config` |
| **revert** | Revert changes | ⏪ | `[revert] Undo breaking changes` |

## 📱 Screenshots

### CLI Mode
```
🚀 Launching Gitt CLI...
📂 Current directory: /home/user/project

Select files to add:
❯ [ALL] Add all changes
  📄 src/main.py
  📝 README.md
  📦 package.json

Select commit type:
❯ feat - Feature
  fix - Fix  
  docs - Documentation

Enter commit message: Add AI-powered commit generation
✅ Commit created: [feat] Add AI-powered commit generation
```

### GUI Mode Features
- 📁 **Visual File Management**: Checkbox selection with git status icons
- 🎨 **Modern Interface**: Clean, intuitive Streamlit design
- 🤖 **AI Integration**: One-click intelligent commit messages
- 👀 **Live Preview**: Real-time diff and commit preview
- ⚡ **Quick Actions**: Add files, commit, refresh status

## 🛠️ Development

### **Project Structure**
```
gitt/
├── gitt.sh                 # Main CLI script
├── gitt_gui.py            # Streamlit GUI application
├── changelog_generator.py  # AI changelog generator
├── install.sh             # Cross-platform installer
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── demo.sh               # Demo setup script
└── test_gui.py           # GUI testing utility
```

### **Contributing**
```bash
# 1. Fork and clone
git clone https://github.com/yourusername/gitt.git
cd gitt

# 2. Setup development environment
./install.sh

# 3. Make changes and test
./demo.sh  # Creates test environment
gitt --gui # Test GUI mode

# 4. Commit using gitt itself!
gitt

# 5. Submit PR
```

## � Configuration

### **File Locations**
- **CLI Script**: `/usr/local/bin/gitt`
- **GUI Components**: `~/.config/gitt/`
- **Virtual Environment**: `~/.config/gitt/.venv/`
- **Configuration**: `~/.config/gitt/.env`

### **Environment Variables**
```bash
GEMINI_API_KEY=your_gemini_api_key_here  # Required for AI features
```

### **Supported Linux Distributions**
- ✅ Ubuntu 18.04+ / Debian 10+
- ✅ CentOS 7+ / RHEL 7+ / Fedora 30+
- ✅ Arch Linux / Manjaro
- ✅ openSUSE Leap / Tumbleweed
- ✅ Alpine Linux 3.12+
- ✅ Any distribution with `python3`, `git`, and `fzf`

## 🚀 Performance

- **CLI Mode**: Lightning fast with `fzf` integration
- **GUI Mode**: Responsive web interface via Streamlit
- **AI Generation**: ~2-3 seconds for commit messages
- **Virtual Environment**: Isolated dependencies, no conflicts

## 📊 Advanced Usage

### **Batch Operations**
```bash
# Multiple projects changelog
for dir in project1 project2 project3; do
  cd $dir && ~/.config/gitt/changelog_generator.py --since "1 week ago"
done
```

### **Custom Commit Templates**
```bash
# Use with conventional commits
gitt  # Select 'feat' type
# Enter: "user authentication with OAuth2"
# Result: [feat] user authentication with OAuth2
```

### **Integration with IDEs**
```bash
# VS Code terminal
gitt --gui  # Opens in browser tab

# Vim/Neovim users
alias gcm='gitt'  # Quick access
```

## 🆘 Troubleshooting

<details>
<summary><strong>Common Issues</strong></summary>

### **"Command not found: gitt"**
```bash
# Ensure /usr/local/bin is in PATH
echo $PATH | grep /usr/local/bin
# If not, add to ~/.bashrc or ~/.zshrc:
export PATH="/usr/local/bin:$PATH"
```

### **"Streamlit not found"**
```bash
# Reinstall dependencies
cd ~/.config/gitt
.venv/bin/pip install -r requirements.txt
```

### **"Port 8501 already in use"**
```bash
# Kill existing streamlit processes
pkill -f streamlit
# Or use different port
.venv/bin/streamlit run gitt_gui.py --server.port 8502
```

### **GUI shows "Not in git repository"**
```bash
# Verify git repository
git status  # Should show git info
# Ensure you're in the right directory
pwd
```

</details>

## 🙏 Acknowledgments

- **[Sina Bayandorian](https://github.com/sina-byn/gitt)** - Original `gitt` inspiration
- **[Google Gemini](https://ai.google.dev/)** - AI-powered commit messages
- **[Streamlit](https://streamlit.io/)** - Beautiful web interface
- **[fzf](https://github.com/junegunn/fzf)** - Fuzzy finder for CLI

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/gitt/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/gitt/discussions)
- ⭐ **Star the repo** if you find it helpful!

---

<div align="center">

**Made with ❤️ for better git workflows**

[⬆ Back to top](#-gitt---enhanced-git-commit-helper-with-ai)

</div>

## 🏷️ Commit Types

| Commit Type | Description | Icon |
|-------------|-------------|------|
| **feat** | A new feature | ✨ |
| **fix** | A bug fix | 🐛 |
| **chore** | Routine tasks and maintenance | 🔧 |
| **refactor** | Code changes that do not affect functionality | ♻️ |
| **docs** | Documentation changes | 📝 |
| **style** | Formatting changes (no code change) | 💄 |
| **test** | Adding or updating tests | ✅ |
| **perf** | Performance improvements | ⚡ |
| **ci** | Changes related to continuous integration | 👷 |
| **build** | Changes related to the build process | 📦 |
| **revert** | Reverting previous changes | ⏪ |
| **none** | No specific type selected | 🔄 |

## 📸 Screenshots

### CLI Mode
```
🚀 Launching Gitt CLI...
Select files to add:
> [ALL] Add all changes
  src/main.py
  README.md
  package.json

Select commit type:
> feat - Feature
  fix - Fix
  docs - Documentation

Enter commit message: Add AI-powered commit generation
✅ Commit created: [feat] Add AI-powered commit generation
```

### GUI Mode
The GUI provides:
- 📁 Visual file selection with status indicators
- 🎨 Modern, intuitive interface
- 🤖 One-click AI commit message generation
- 👀 Real-time diff preview
- ⚡ Instant commit execution

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### File Locations
- **CLI Script**: `/usr/local/bin/gitt`
- **GUI Components**: `~/.config/gitt/`
- **Config Files**: `~/.config/gitt/.env`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✨ Commit your changes (`gitt` - use the tool itself!)
4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎯 Open a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/gitt
cd gitt
pip install -r requirements.txt
cp .env.example .env
# Add your Gemini API key to .env
```

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## 🙏 Acknowledgments

This project was inspired by the work of [Sina Bayandorian](https://github.com/sina-byn/gitt), whose original `gitt` project provided valuable insights into creating a CLI for better commit messages.

Special thanks to:
- 🤖 Google Gemini AI for intelligent commit message generation
- 🎨 Streamlit for the beautiful web interface
- 🔍 fzf for excellent terminal-based selection UI

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. 📖 Check the documentation above
2. 🐛 Open an issue on GitHub
3. 💬 Start a discussion for feature requests

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐