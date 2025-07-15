#!/bin/bash

# Demo script for testing gitt functionality
# This script creates a test environment to showcase gitt features

echo "🎬 Gitt Demo Setup"
echo "=================="

# Create a temporary demo directory
DEMO_DIR="/tmp/gitt_demo_$(date +%s)"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"

echo "📁 Created demo directory: $DEMO_DIR"

# Initialize git repository
git init
git config user.name "Demo User"
git config user.email "demo@example.com"

echo "🎯 Initialized git repository"

# Create some demo files with realistic content
mkdir -p src tests docs

cat > README.md << 'EOF'
# Demo Project

This is a demo project to showcase gitt functionality.

## Features

- Smart commit message generation
- AI-powered changelog creation
- Cross-platform compatibility
- Modern GUI interface

## Usage

```bash
npm start
```

## Contributing

Please use gitt for consistent commit messages!
EOF

cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application module for the demo project.
"""

import sys
from typing import List, Optional

class DemoApp:
    """Main application class."""
    
    def __init__(self, name: str = "Gitt Demo"):
        self.name = name
        self.version = "1.0.0"
    
    def greet(self, user: Optional[str] = None) -> str:
        """Generate a greeting message."""
        if user:
            return f"Hello, {user}! Welcome to {self.name}"
        return f"Hello! Welcome to {self.name}"
    
    def run(self) -> int:
        """Run the application."""
        print(self.greet())
        print(f"Version: {self.version}")
        return 0

def main() -> int:
    """Main entry point."""
    app = DemoApp()
    return app.run()

if __name__ == "__main__":
    sys.exit(main())
EOF

cat > src/utils.py << 'EOF'
"""
Utility functions for the demo project.
"""

from typing import Any, Dict, List
import json

def format_data(data: Dict[str, Any]) -> str:
    """Format dictionary data as JSON string."""
    return json.dumps(data, indent=2)

def validate_email(email: str) -> bool:
    """Simple email validation."""
    return "@" in email and "." in email.split("@")[1]

def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        return {"count": 0, "sum": 0, "mean": 0, "min": 0, "max": 0}
    
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers)
    }
EOF

cat > tests/test_main.py << 'EOF'
"""
Tests for the main module.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import DemoApp

class TestDemoApp(unittest.TestCase):
    """Test cases for DemoApp class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = DemoApp("Test App")
    
    def test_greet_with_user(self):
        """Test greeting with user name."""
        result = self.app.greet("Alice")
        self.assertIn("Alice", result)
        self.assertIn("Test App", result)
    
    def test_greet_without_user(self):
        """Test greeting without user name."""
        result = self.app.greet()
        self.assertIn("Test App", result)
        self.assertNotIn("None", result)

if __name__ == '__main__':
    unittest.main()
EOF

cat > package.json << 'EOF'
{
  "name": "gitt-demo",
  "version": "1.0.0",
  "description": "Demo project for testing gitt functionality",
  "main": "src/main.py",
  "scripts": {
    "start": "python3 src/main.py",
    "test": "python3 -m pytest tests/",
    "lint": "python3 -m flake8 src/"
  },
  "keywords": ["git", "demo", "gitt", "commit"],
  "author": "Gitt Demo",
  "license": "MIT",
  "devDependencies": {
    "pytest": "^7.0.0",
    "flake8": "^5.0.0"
  }
}
EOF

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.coverage
.pytest_cache/

# Virtual environments
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF

cat > docs/API.md << 'EOF'
# API Documentation

## DemoApp Class

### Methods

#### `greet(user: Optional[str] = None) -> str`
Generate a personalized greeting message.

**Parameters:**
- `user`: Optional username for personalization

**Returns:**
- Formatted greeting string

#### `run() -> int`
Execute the main application logic.

**Returns:**
- Exit code (0 for success)

## Utility Functions

### `format_data(data: Dict[str, Any]) -> str`
Convert dictionary to formatted JSON string.

### `validate_email(email: str) -> bool`
Perform basic email validation.

### `calculate_stats(numbers: List[float]) -> Dict[str, float]`
Calculate statistical measures for numeric data.
EOF

echo "📝 Created demo files with realistic content"

# Add some initial commits to make it more realistic
git add README.md
git commit -m "[docs] Add project README with basic information"

git add package.json .gitignore
git commit -m "[chore] Setup project configuration and gitignore"

git add src/main.py
git commit -m "[feat] Add main application class with greeting functionality"

# Show current status
echo ""
echo "🔍 Current git status:"
git status

echo ""
echo "📊 Git history:"
git log --oneline

echo ""
echo "🚀 Demo environment ready!"
echo ""
echo "📂 Demo directory: $DEMO_DIR"
echo ""
echo "You can now test gitt in this directory:"
echo "  cd $DEMO_DIR"
echo "  gitt          # CLI mode"
echo "  gitt --gui    # GUI mode"
echo ""
echo "Available changes to commit:"
echo "  - 📄 src/utils.py (new utility functions)"
echo "  - 📄 tests/test_main.py (unit tests)"
echo "  - 📄 docs/API.md (API documentation)"
echo ""
echo "Try these commit types:"
echo "  - [feat] for new features"
echo "  - [test] for adding tests"  
echo "  - [docs] for documentation"
echo ""
echo "🧹 To clean up later: rm -rf $DEMO_DIR"
echo ""
echo "💡 Pro tip: Use 'gitt --gui' to try the AI-powered commit message generation!"
