import os
import sys
# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)
from Update_Git import git_add, git_commit, git_push

# Update Git Repository
file_path = os.path.join(current_path, "Try.py")
git_add(file_path)
git_commit("Update Try.py")
git_push("main")
