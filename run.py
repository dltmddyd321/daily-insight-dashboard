import subprocess
import os
import sys
import webbrowser
import time

def run_command(command, cwd=None):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: Command failed with return code {result.returncode}")
        return False
    return True

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("==========================================")
    print("   Daily Insight Dashboard Starter")
    print("==========================================")

    # 1. Install Dependencies
    print("\n[1/3] Checking dependencies...")
    requirements_path = os.path.join(project_root, "requirements.txt")
    if not run_command(f"{sys.executable} -m pip install -r {requirements_path} -q"):
        print("Dependency installation failed.")
        return

    # 2. Run Backend
    print("\n[2/3] Fetching emails and generating insights...")
    backend_main = os.path.join(project_root, "backend", "main.py")
    if not run_command(f"{sys.executable} {backend_main}"):
        print("Backend execution failed.")
        return

    # 3. Open Frontend
    print("\n[3/3] Opening Dashboard...")
    frontend_html = os.path.join(project_root, "frontend", "index.html")
    file_url = "file://" + os.path.abspath(frontend_html).replace("\\", "/")
    
    print(f"Opening: {file_url}")
    webbrowser.open(file_url)

    print("\nDone! Have a productive day.")

if __name__ == "__main__":
    main()
