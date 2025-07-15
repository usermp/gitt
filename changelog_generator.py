#!/usr/bin/env python3

"""
Changelog Generator with Gemini AI
Automatically generates changelog entries from git commit history
"""

import argparse
import subprocess
import os
import sys
from datetime import datetime

# Try to load optional dependencies
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class ChangelogGenerator:
    def __init__(self):
        if GEMINI_AVAILABLE:
            self.setup_gemini()
        else:
            print("⚠️  Google Generative AI not available. Using basic changelog generation.")
            self.model = None
    
    def setup_gemini(self):
        """Setup Gemini AI client"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY not found in environment variables")
            print("💡 AI features will be disabled. Using basic changelog generation.")
            self.model = None
            return
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_git_commits(self, since=None, until=None, format_type="detailed"):
        """Get git commits with specified filters"""
        try:
            cmd = ['git', 'log', '--oneline']
            
            if since:
                cmd.extend(['--since', since])
            if until:
                cmd.extend(['--until', until])
            
            if format_type == "detailed":
                cmd = ['git', 'log', '--pretty=format:%h|%ad|%an|%s', '--date=short']
                if since:
                    cmd.extend(['--since', since])
                if until:
                    cmd.extend(['--until', until])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting git commits: {e}")
            return []
    
    def parse_commits(self, commits):
        """Parse commit data into structured format"""
        parsed_commits = []
        
        for commit in commits:
            if '|' in commit:
                parts = commit.split('|', 3)
                if len(parts) >= 4:
                    hash_short, date, author, message = parts
                    
                    # Detect commit type from message
                    commit_type = "other"
                    if message.startswith('['):
                        end_bracket = message.find(']')
                        if end_bracket > 0:
                            commit_type = message[1:end_bracket].lower()
                            message = message[end_bracket + 1:].strip()
                    
                    parsed_commits.append({
                        'hash': hash_short,
                        'date': date,
                        'author': author,
                        'message': message,
                        'type': commit_type
                    })
        
        return parsed_commits
    
    def categorize_commits(self, commits):
        """Categorize commits by type"""
        categories = {
            'feat': [],
            'fix': [],
            'chore': [],
            'refactor': [],
            'docs': [],
            'style': [],
            'test': [],
            'perf': [],
            'ci': [],
            'build': [],
            'revert': [],
            'other': []
        }
        
        for commit in commits:
            commit_type = commit.get('type', 'other')
            if commit_type in categories:
                categories[commit_type].append(commit)
            else:
                categories['other'].append(commit)
        
        return categories
    
    def generate_ai_changelog(self, commits, version=None):
        """Generate changelog using Gemini AI"""
        if not commits:
            return "No commits found for the specified period."
        
        if not self.model:
            print("⚠️  AI not available, falling back to basic changelog generation")
            return self.generate_basic_changelog(commits, version)

        commits_text = "\n".join([
            f"- [{commit['type']}] {commit['message']} ({commit['hash']}) by {commit['author']} on {commit['date']}"
            for commit in commits
        ])
        
        prompt = f"""
        Generate a professional changelog entry from the following git commits.
        
        Guidelines:
        1. Group commits by type (Features, Bug Fixes, Chores, etc.)
        2. Use clear, user-friendly language
        3. Focus on user-facing changes
        4. Include commit hashes for reference
        5. Use markdown formatting
        6. Be concise but descriptive
        
        {f"Version: {version}" if version else ""}
        
        Commits:
        {commits_text}
        
        Generate a markdown changelog entry:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error generating AI changelog: {e}")
            return self.generate_basic_changelog(commits, version)
    
    def generate_basic_changelog(self, commits, version=None):
        """Generate basic changelog without AI"""
        categorized = self.categorize_commits(commits)
        
        changelog = []
        
        # Add version header
        if version:
            changelog.append(f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}")
        else:
            changelog.append(f"## Unreleased - {datetime.now().strftime('%Y-%m-%d')}")
        changelog.append("")
        
        # Add categories with commits
        category_titles = {
            'feat': '### ✨ Features',
            'fix': '### 🐛 Bug Fixes',
            'perf': '### ⚡ Performance',
            'refactor': '### ♻️ Refactoring',
            'docs': '### 📝 Documentation',
            'style': '### 💄 Style',
            'test': '### ✅ Tests',
            'chore': '### 🔧 Chores',
            'ci': '### 👷 CI/CD',
            'build': '### 📦 Build',
            'revert': '### ⏪ Reverts'
        }
        
        for category, title in category_titles.items():
            commits_in_category = categorized.get(category, [])
            if commits_in_category:
                changelog.append(title)
                for commit in commits_in_category:
                    changelog.append(f"- {commit['message']} ([{commit['hash']}]) by {commit['author']}")
                changelog.append("")
        
        # Add other commits if any
        if categorized.get('other'):
            changelog.append("### 🔄 Other Changes")
            for commit in categorized['other']:
                changelog.append(f"- {commit['message']} ([{commit['hash']}]) by {commit['author']}")
            changelog.append("")
        
        return '\n'.join(changelog)
    
    def save_changelog(self, content, output_file="CHANGELOG.md", append=True):
        """Save changelog to file"""
        try:
            mode = 'a' if append and os.path.exists(output_file) else 'w'
            
            if append and os.path.exists(output_file):
                # Read existing content and prepend new content
                with open(output_file, 'r') as f:
                    existing_content = f.read()
                
                with open(output_file, 'w') as f:
                    f.write(content + '\n\n' + existing_content)
            else:
                with open(output_file, 'w') as f:
                    f.write(content)
            
            print(f"✅ Changelog saved to {output_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving changelog: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Generate changelog from git commits using Gemini AI")
    parser.add_argument('--since', help='Include commits since this date (e.g., "2024-01-01", "1 week ago")')
    parser.add_argument('--until', help='Include commits until this date')
    parser.add_argument('--version', help='Version number for the changelog entry')
    parser.add_argument('--output', default='CHANGELOG.md', help='Output file (default: CHANGELOG.md)')
    parser.add_argument('--no-ai', action='store_true', help='Generate basic changelog without AI')
    parser.add_argument('--print-only', action='store_true', help='Print changelog to stdout only')
    
    args = parser.parse_args()
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Error: Not in a git repository")
        sys.exit(1)
    
    generator = ChangelogGenerator()
    
    print("📝 Generating changelog...")
    
    # Get commits
    commits = generator.get_git_commits(since=args.since, until=args.until)
    
    if not commits:
        print("ℹ️ No commits found for the specified criteria")
        return
    
    parsed_commits = generator.parse_commits(commits)
    print(f"📊 Found {len(parsed_commits)} commits")
    
    # Generate changelog
    if args.no_ai or not GEMINI_AVAILABLE or not os.getenv('GEMINI_API_KEY'):
        if not args.no_ai and not GEMINI_AVAILABLE:
            print("⚠️ Gemini AI dependencies not available, using basic changelog generation")
        elif not args.no_ai and not os.getenv('GEMINI_API_KEY'):
            print("⚠️ Gemini API key not found, using basic changelog generation")
        changelog = generator.generate_basic_changelog(parsed_commits, args.version)
    else:
        print("🤖 Generating AI-powered changelog...")
        changelog = generator.generate_ai_changelog(parsed_commits, args.version)
    
    # Output changelog
    if args.print_only:
        print("\n" + "="*50)
        print("GENERATED CHANGELOG")
        print("="*50)
        print(changelog)
    else:
        if generator.save_changelog(changelog, args.output):
            print(f"📄 Changelog generated successfully!")
            if not args.print_only:
                print("\nPreview:")
                print("-" * 40)
                # Show first few lines
                lines = changelog.split('\n')
                for line in lines[:10]:
                    print(line)
                if len(lines) > 10:
                    print("... (truncated)")

if __name__ == "__main__":
    main()
