import streamlit as st
import subprocess
import os
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Configure Gemini API
try:
    import google.generativeai as genai
    if os.getenv('GEMINI_API_KEY'):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class GitHelper:
    def __init__(self):
        self.commit_types = {
            "feat": "Feature",
            "fix": "Fix", 
            "chore": "Chore",
            "refactor": "Refactor",
            "docs": "Documentation",
            "style": "Style",
            "test": "Test",
            "perf": "Performance",
            "ci": "Continuous Integration",
            "build": "Build",
            "revert": "Revert"
        }
    
    def is_git_repository(self):
        """Check if current directory is a git repository"""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], 
                          capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_git_status(self):
        """Get git status and changed files"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    files.append({"status": status, "filename": filename})
            return files
        except subprocess.CalledProcessError:
            return []
    
    def get_git_diff(self, files=None):
        """Get git diff for specified files or all changes"""
        try:
            cmd = ['git', 'diff', '--cached']
            if files and files != ["."]:
                cmd.append('--')
                cmd.extend(files)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if not result.stdout:
                # If no staged changes, get unstaged diff
                cmd = ['git', 'diff']
                if files and files != ["."]:
                    cmd.append('--')
                    cmd.extend(files)
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def get_file_stats(self, files=None):
        """Get file statistics (lines added/removed) for specified files"""
        try:
            cmd = ['git', 'diff', '--stat', '--cached']
            if files and files != ["."]:
                cmd.append('--')
                cmd.extend(files)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if not result.stdout:
                # If no staged changes, get unstaged stats
                cmd = ['git', 'diff', '--stat']
                if files and files != ["."]:
                    cmd.append('--')
                    cmd.extend(files)
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def get_file_changes_summary(self, files=None):
        """Get a detailed summary of changes for each file"""
        try:
            file_changes = {}
            
            # Get list of changed files with their status
            cmd = ['git', 'status', '--porcelain']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if files and files != ["."]:
                # Filter to only specified files
                all_files = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        filename = line[3:]
                        if filename in files:
                            all_files.append(line)
                status_output = '\n'.join(all_files)
            else:
                status_output = result.stdout
            
            # Parse each file's changes
            for line in status_output.strip().split('\n'):
                if line.strip():
                    status = line[:2]
                    filename = line[3:]
                    
                    # Determine change type
                    if status == "A ":
                        change_type = "Added"
                    elif status == "M " or status == " M":
                        change_type = "Modified"
                    elif status == "D ":
                        change_type = "Deleted"
                    elif status == "R ":
                        change_type = "Renamed"
                    elif status == "??":
                        change_type = "New file"
                    else:
                        change_type = "Changed"
                    
                    # Get file-specific diff for new insights (with better error handling)
                    file_diff = ""
                    try:
                        # Try staged changes first
                        if status.strip() and status[0] != '?':  # Not untracked
                            file_diff_cmd = ['git', 'diff', '--cached', '--', filename]
                            file_diff_result = subprocess.run(file_diff_cmd, capture_output=True, text=True)
                            if file_diff_result.returncode == 0 and file_diff_result.stdout:
                                file_diff = file_diff_result.stdout
                            else:
                                # Try unstaged changes
                                file_diff_cmd = ['git', 'diff', '--', filename]
                                file_diff_result = subprocess.run(file_diff_cmd, capture_output=True, text=True)
                                if file_diff_result.returncode == 0:
                                    file_diff = file_diff_result.stdout
                    except Exception as e:
                        # If git diff fails, just continue without diff content
                        file_diff = f"(Error getting diff: {str(e)})"
                    
                    file_changes[filename] = {
                        "type": change_type,
                        "diff": file_diff
                    }
            
            return file_changes
        except subprocess.CalledProcessError as e:
            # Return empty dict on git command failure
            return {}
    
    def get_recent_commits_context(self, limit=5):
        """Get recent commit messages for context"""
        try:
            cmd = ['git', 'log', '--oneline', f'-{limit}']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
    
    def add_files(self, files):
        """Add files to git staging area"""
        try:
            if files == ["."]:
                subprocess.run(['git', 'add', '.'], check=True)
            else:
                subprocess.run(['git', 'add'] + files, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def commit(self, message):
        """Create git commit with message"""
        try:
            subprocess.run(['git', 'commit', '-m', message], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def generate_commit_message(self, diff_content, commit_type=None, selected_files=None):
        """Generate detailed commit message using Gemini API with changelog analysis"""
        if not GEMINI_AVAILABLE:
            return "Gemini AI not available - please install google-generativeai"
        
        if not os.getenv('GEMINI_API_KEY'):
            return "No Gemini API key configured"
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Get additional context for better commit messages
            file_changes = self.get_file_changes_summary(selected_files)
            file_stats = self.get_file_stats(selected_files)
            recent_commits = self.get_recent_commits_context()
            
            # Build file change summary
            change_summary = ""
            if file_changes:
                change_summary = "\n\nFile Changes Summary:\n"
                for filename, info in file_changes.items():
                    change_summary += f"- {filename}: {info['type']}\n"
            
            # Determine commit type context
            type_context = ""
            if commit_type and commit_type != "none":
                type_context = f"\nCommit Type: {commit_type} ({self.commit_types.get(commit_type, '')})"
            
            prompt = f"""
            Generate a detailed commit message based on the following git changes. The commit message should follow this format:

            [type] Brief title (under 50 characters)

            Detailed description explaining what was changed and why.

            For multiple files, group related changes and explain the overall impact.

            Guidelines:
            1. Title should be concise and use imperative mood (e.g., "Add", "Fix", "Update")
            2. Don't include the commit type prefix in the title - it will be added automatically
            3. Provide a detailed description in the body explaining:
               - What files were changed and how
               - The purpose of the changes
               - Any new features or improvements added
            4. Group related changes together
            5. Be specific about functionality added, fixed, or improved

            {type_context}

            File Statistics:
            {file_stats}
            {change_summary}

            Recent Commit History (for context):
            {recent_commits}

            Git Diff:
            {diff_content}

            Generate a commit message that provides clear understanding of what changed:
            """
            
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating message: {str(e)}"

def main():
    st.set_page_config(
        page_title="Gitt - Git Commit Helper",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Gitt - Smart Git Commit Helper")
    st.markdown("A modern GUI for better git commits with AI-powered commit messages")
    
    # --- Select Git Project Directory ---
    st.sidebar.header("Select Git Project Directory")
    import glob
    import pathlib
    # List subdirectories in home and current dir for quick selection
    home = str(pathlib.Path.home())
    cwd = os.getcwd()
    quick_dirs = [cwd, home] + glob.glob(f"{home}/*/")
    quick_dirs = [d for d in quick_dirs if os.path.isdir(d)]
    default_dir = st.session_state.get("selected_git_dir", cwd)
    selected_git_dir = st.sidebar.selectbox(
        "Quick Select Directory", quick_dirs, index=quick_dirs.index(default_dir) if default_dir in quick_dirs else 0
    )
    custom_dir = st.sidebar.text_input(
        "Or enter custom path", value=selected_git_dir, help="Enter or paste the path to your git project directory"
    )
    if st.sidebar.button("Set Project Directory"):
        if os.path.isdir(custom_dir):
            st.session_state.selected_git_dir = custom_dir
            st.success(f"Project directory set to: {custom_dir}")
        else:
            st.error("❌ Invalid directory. Please select a valid path.")
    current_dir = st.session_state.get("selected_git_dir", cwd)
    st.caption(f"📂 Working directory: `{current_dir}`")
    
    # Helper to run git commands in selected directory
    class GitHelperWithPath(GitHelper):
        def _run(self, cmd, **kwargs):
            return subprocess.run(cmd, cwd=current_dir, **kwargs)
        def is_git_repository(self):
            try:
                self._run(['git', 'rev-parse', '--git-dir'], capture_output=True, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        def get_git_status(self):
            try:
                result = self._run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
                files = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        status = line[:2]
                        filename = line[3:]
                        files.append({"status": status, "filename": filename})
                return files
            except subprocess.CalledProcessError:
                return []
        def get_git_diff(self, files=None):
            try:
                cmd = ['git', 'diff', '--cached']
                if files and files != ["."]:
                    cmd.append('--')
                    cmd.extend(files)
                result = self._run(cmd, capture_output=True, text=True, check=True)
                if not result.stdout:
                    cmd = ['git', 'diff']
                    if files and files != ["."]:
                        cmd.append('--')
                        cmd.extend(files)
                    result = self._run(cmd, capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError:
                return ""
        def get_file_stats(self, files=None):
            try:
                cmd = ['git', 'diff', '--stat', '--cached']
                if files and files != ["."]:
                    cmd.append('--')
                    cmd.extend(files)
                result = self._run(cmd, capture_output=True, text=True, check=True)
                if not result.stdout:
                    cmd = ['git', 'diff', '--stat']
                    if files and files != ["."]:
                        cmd.append('--')
                        cmd.extend(files)
                    result = self._run(cmd, capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError:
                return ""
        def get_file_changes_summary(self, files=None):
            try:
                file_changes = {}
                cmd = ['git', 'status', '--porcelain']
                result = self._run(cmd, capture_output=True, text=True, check=True)
                if files and files != ["."]:
                    all_files = []
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            filename = line[3:]
                            if filename in files:
                                all_files.append(line)
                    status_output = '\n'.join(all_files)
                else:
                    status_output = result.stdout
                for line in status_output.strip().split('\n'):
                    if line.strip():
                        status = line[:2]
                        filename = line[3:]
                        change_type = "Changed"
                        if status == "A ":
                            change_type = "Added"
                        elif status == "M " or status == " M":
                            change_type = "Modified"
                        elif status == "D ":
                            change_type = "Deleted"
                        elif status == "R ":
                            change_type = "Renamed"
                        elif status == "??":
                            change_type = "New file"
                        file_diff = ""
                        try:
                            if status.strip() and status[0] != '?':
                                file_diff_cmd = ['git', 'diff', '--cached', '--', filename]
                                file_diff_result = self._run(file_diff_cmd, capture_output=True, text=True)
                                if file_diff_result.returncode == 0 and file_diff_result.stdout:
                                    file_diff = file_diff_result.stdout
                                else:
                                    file_diff_cmd = ['git', 'diff', '--', filename]
                                    file_diff_result = self._run(file_diff_cmd, capture_output=True, text=True)
                                    if file_diff_result.returncode == 0:
                                        file_diff = file_diff_result.stdout
                        except Exception as e:
                            file_diff = f"(Error getting diff: {str(e)})"
                        file_changes[filename] = {"type": change_type, "diff": file_diff}
                return file_changes
            except subprocess.CalledProcessError:
                return {}
        def get_recent_commits_context(self, limit=5):
            try:
                cmd = ['git', 'log', '--oneline', f'-{limit}']
                result = self._run(cmd, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                return ""
        def add_files(self, files):
            try:
                if files == ["."]:
                    self._run(['git', 'add', '.'], check=True)
                else:
                    self._run(['git', 'add'] + files, check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        def commit(self, message):
            try:
                self._run(['git', 'commit', '-m', message], check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        def generate_commit_message(self, diff_content, commit_type=None, selected_files=None):
            return super().generate_commit_message(diff_content, commit_type, selected_files)
    
    git_helper = GitHelperWithPath()
    
    # Check if we're in a git repository
    if not git_helper.is_git_repository():
        st.error("❌ Not in a git repository. Please select a valid git project directory from the sidebar.")
        st.info("💡 Make sure your selected directory contains a .git folder.")
        st.code(f"Current directory: {current_dir}")
        return
    
    # Check API key configuration
    with st.expander("🔑 API Key Configuration", expanded=not bool(os.getenv('GEMINI_API_KEY'))):
        if not GEMINI_AVAILABLE:
            st.error("❌ Gemini AI package not available. Install with: pip install google-generativeai")
        elif not os.getenv('GEMINI_API_KEY'):
            st.warning("⚠️ Gemini API key not configured.")
            st.info("💡 Configure your API key below to enable AI features.")
            
            # API key input
            col1, col2 = st.columns([3, 1])
            with col1:
                api_key_input = st.text_input(
                    "Gemini API Key", 
                    type="password",
                    placeholder="Enter your Gemini API key here...",
                    help="Get your free API key from https://makersuite.google.com/app/apikey"
                )
            with col2:
                if st.button("💾 Save Key", type="primary"):
                    if api_key_input.strip():
                        # Save API key to .env file
                        config_dir = os.path.expanduser("~/.config/gitt")
                        os.makedirs(config_dir, exist_ok=True)
                        env_file = os.path.join(config_dir, ".env")
                        
                        # Update or create .env file
                        env_content = ""
                        if os.path.exists(env_file):
                            with open(env_file, 'r') as f:
                                env_content = f.read()
                        
                        # Update or add API key
                        if 'GEMINI_API_KEY=' in env_content:
                            import re
                            env_content = re.sub(r'GEMINI_API_KEY=.*', f'GEMINI_API_KEY={api_key_input.strip()}', env_content)
                        else:
                            env_content += f"\nGEMINI_API_KEY={api_key_input.strip()}\n"
                        
                        with open(env_file, 'w') as f:
                            f.write(env_content)
                        
                        # Set secure permissions
                        os.chmod(env_file, 0o600)
                        
                        st.success("✅ API key saved! Please refresh the page to enable AI features.")
                        st.info("🔄 Refresh this page (F5) to activate AI features.")
                    else:
                        st.error("❌ Please enter a valid API key")
            
            st.markdown("---")
            st.markdown("**How to get your API key:**")
            st.markdown("1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)")
            st.markdown("2. Sign in with your Google account")
            st.markdown("3. Click 'Create API Key'")
            st.markdown("4. Copy the key and paste it above")
        else:
            st.success("✅ AI features are ready!")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"🔑 API key configured (ends with: ...{os.getenv('GEMINI_API_KEY', '')[-4:]})")
            with col2:
                if st.button("🔄 Update Key"):
                    # Clear the current session to show input again
                    if 'api_key_configured' in st.session_state:
                        del st.session_state.api_key_configured
                    st.experimental_rerun()
    
    # Get git status
    files = git_helper.get_git_status()
    
    if not files:
        st.info("✅ No changes detected in the repository.")
        return
    
    # Display current changes
    st.subheader("📁 Changed Files")
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Select files to add:**")
        
        # Add option to select all files
        add_all = st.checkbox("📦 Add all changes", key="add_all")
        
        selected_files = []
        if not add_all:
            for file_info in files:
                status = file_info["status"]
                filename = file_info["filename"]
                
                # Status icons
                status_icon = {
                    "M ": "✏️",  # Modified
                    " M": "✏️",  # Modified (unstaged)
                    "A ": "➕",  # Added
                    "D ": "🗑️",  # Deleted
                    "R ": "🔄",  # Renamed
                    "??": "❓"   # Untracked
                }.get(status, "📄")
                
                if st.checkbox(f"{status_icon} {filename}", key=f"file_{filename}"):
                    selected_files.append(filename)
        else:
            selected_files = ["."]
    
    with col2:
        st.markdown("**Commit Configuration:**")
        
        # Commit type selection
        commit_type = st.selectbox(
            "🏷️ Commit Type",
            ["none"] + list(git_helper.commit_types.keys()),
            format_func=lambda x: "No specific type" if x == "none" else f"{x} - {git_helper.commit_types.get(x, '')}"
        )
        
        # AI-powered commit message generation
        ai_available = GEMINI_AVAILABLE and os.getenv('GEMINI_API_KEY')
        
        st.markdown("**🤖 AI-Powered Commit Messages**")
        st.info("🔍 AI analyzes file changes, diffs, and git history to generate detailed, contextual commit messages")
        
        if st.button("🤖 Generate AI Commit Message", disabled=not ai_available):
            if not ai_available:
                if not GEMINI_AVAILABLE:
                    st.error("❌ Gemini AI not installed. Run: pip install google-generativeai")
                else:
                    st.error("❌ Gemini API key not configured")
            elif selected_files:
                with st.spinner("Generating detailed commit message..."):
                    # First add files to see the diff
                    temp_files = selected_files if selected_files != ["."] else None
                    if git_helper.add_files(selected_files):
                        diff_content = git_helper.get_git_diff()
                        if diff_content:
                            ai_message = git_helper.generate_commit_message(
                                diff_content, 
                                git_helper.commit_types.get(commit_type) if commit_type != "none" else None,
                                selected_files
                            )
                            st.session_state.ai_message = ai_message
                        else:
                            st.warning("No diff content available for AI generation")
                    else:
                        st.error("Failed to add files")
            else:
                st.warning("Please select files first")
        
        # Commit message input
        default_message = st.session_state.get('ai_message', '')
        commit_message = st.text_area(
            "💬 Commit Message", 
            value=default_message,
            height=200,
            placeholder="Enter your commit message here...\n\nFor detailed messages, use:\n[title]\n\nDetailed description here..."
        )
    
    # Preview section
    if commit_message:
        st.subheader("👀 Commit Preview")
        
        # Format final commit message
        if commit_type == "none":
            final_message = commit_message
        else:
            # Check if the message already has a type prefix
            if commit_message.strip().startswith('[') and ']' in commit_message:
                final_message = commit_message
            else:
                final_message = f"[{commit_type}] {commit_message}"
        
        # Display the commit message with better formatting
        st.markdown("**Full Commit Message:**")
        st.code(final_message, language="text")
        
        # Show message statistics
        lines = final_message.split('\n')
        title_line = lines[0] if lines else ""
        body_lines = lines[1:] if len(lines) > 1 else []
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Title Length", len(title_line), delta=f"{50-len(title_line)} chars remaining")
        with col2:
            st.metric("Total Lines", len(lines))
        with col3:
            st.metric("Body Lines", len([l for l in body_lines if l.strip()]))
        
        # Files to be committed
        if selected_files:
            st.markdown("**Files to be committed:**")
            for file in selected_files:
                if file == ".":
                    st.markdown("- 📦 All changes")
                else:
                    st.markdown(f"- 📄 {file}")
    
    # Commit actions
    st.subheader("🚀 Actions")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("➕ Add Files", type="secondary"):
            if selected_files:
                if git_helper.add_files(selected_files):
                    st.success("✅ Files added to staging area")
                    st.experimental_rerun()
                else:
                    st.error("❌ Failed to add files")
            else:
                st.warning("⚠️ Please select files to add")
    
    with col2:
        if st.button("💾 Commit Changes", type="primary"):
            if not selected_files:
                st.error("❌ Please select files to commit")
            elif not commit_message.strip():
                st.error("❌ Please enter a commit message")
            else:
                # Add files first
                if git_helper.add_files(selected_files):
                    # Format and commit
                    if commit_type == "none":
                        final_message = commit_message
                    else:
                        # Check if the message already has a type prefix
                        if commit_message.strip().startswith('[') and ']' in commit_message:
                            final_message = commit_message
                        else:
                            final_message = f"[{commit_type}] {commit_message}"
                    
                    if git_helper.commit(final_message):
                        st.success("🎉 Commit created successfully!")
                        st.balloons()
                        # Clear the form
                        st.session_state.ai_message = ""
                        st.experimental_rerun()
                    else:
                        st.error("❌ Failed to create commit")
                else:
                    st.error("❌ Failed to add files")
    
    with col3:
        if st.button("🔄 Refresh Status"):
            st.experimental_rerun()
    
    # Show git diff preview
    if selected_files and st.checkbox("🔍 Show Diff Preview"):
        diff_content = git_helper.get_git_diff(selected_files if selected_files != ["."] else None)
        if diff_content:
            st.subheader("📝 Diff Preview")
            st.code(diff_content, language="diff")
        else:
            st.info("No diff available (files may need to be added first)")
    
    # Show file analysis for AI context
    if selected_files and st.checkbox("📊 Show File Analysis", help="See what the AI analyzes for commit message generation"):
        with st.expander("File Change Analysis", expanded=True):
            file_changes = git_helper.get_file_changes_summary(selected_files)
            file_stats = git_helper.get_file_stats(selected_files)
            
            if file_changes:
                st.markdown("**File Changes:**")
                for filename, info in file_changes.items():
                    st.markdown(f"- **{filename}**: {info['type']}")
            
            if file_stats:
                st.markdown("**Statistics:**")
                st.code(file_stats, language="text")
            
            recent_commits = git_helper.get_recent_commits_context()
            if recent_commits:
                st.markdown("**Recent Commits (for context):**")
                st.code(recent_commits, language="text")

if __name__ == "__main__":
    main()
