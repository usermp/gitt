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
            if files:
                cmd.extend(files)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if not result.stdout:
                # If no staged changes, get unstaged diff
                cmd = ['git', 'diff']
                if files:
                    cmd.extend(files)
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return result.stdout
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
    
    def generate_commit_message(self, diff_content, commit_type=None):
        """Generate commit message using Gemini API"""
        if not GEMINI_AVAILABLE:
            return "Gemini AI not available - please install google-generativeai"
        
        if not os.getenv('GEMINI_API_KEY'):
            return "No Gemini API key configured"
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Based on the following git diff, generate a concise and descriptive commit message.
            
            Rules:
            1. Keep it under 50 characters for the title
            2. Be specific about what changed
            3. Use imperative mood (e.g., "Add", "Fix", "Update")
            4. Don't include the commit type prefix (e.g., [feat], [fix]) - just the message
            
            {f"Commit type context: {commit_type}" if commit_type else ""}
            
            Git diff:
            {diff_content}
            
            Generate only the commit message, nothing else:
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
    
    # Show current working directory
    current_dir = os.getcwd()
    st.caption(f"📂 Working directory: `{current_dir}`")
    
    git_helper = GitHelper()
    
    # Check if we're in a git repository
    if not git_helper.is_git_repository():
        st.error("❌ Not in a git repository. Please navigate to a git repository first.")
        st.info("💡 Make sure you're running this from within a git repository directory.")
        
        # Show current working directory for debugging
        current_dir = os.getcwd()
        st.code(f"Current directory: {current_dir}")
        
        # Show git status to help debug
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode != 0:
                st.error(f"Git error: {result.stderr}")
        except Exception as e:
            st.error(f"Git command failed: {e}")
        
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
        if st.button("🤖 Generate AI Commit Message", disabled=not ai_available):
            if not ai_available:
                if not GEMINI_AVAILABLE:
                    st.error("❌ Gemini AI not installed. Run: pip install google-generativeai")
                else:
                    st.error("❌ Gemini API key not configured")
            elif selected_files:
                with st.spinner("Generating commit message..."):
                    # First add files to see the diff
                    temp_files = selected_files if selected_files != ["."] else None
                    if git_helper.add_files(selected_files):
                        diff_content = git_helper.get_git_diff()
                        if diff_content:
                            ai_message = git_helper.generate_commit_message(
                                diff_content, 
                                git_helper.commit_types.get(commit_type) if commit_type != "none" else None
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
            height=100,
            placeholder="Enter your commit message here..."
        )
    
    # Preview section
    if commit_message:
        st.subheader("👀 Commit Preview")
        
        # Format final commit message
        if commit_type == "none":
            final_message = commit_message
        else:
            final_message = f"[{commit_type}] {commit_message}"
        
        st.code(final_message, language="text")
        
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

if __name__ == "__main__":
    main()
