import subprocess
import os
import sys
import webbrowser
import time
import signal

def run_command(command, cwd=None):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: Command failed with return code {result.returncode}")
        return False
    return True

def start_api_server(project_root):
    print("\n[2/3] Starting API server...")
    api_path = os.path.join(project_root, "backend", "api.py")
    
    # Start the server as a background process
    proc = subprocess.Popen([sys.executable, api_path], cwd=project_root)
    return proc

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

    # 2. Start API Server
    server_proc = start_api_server(project_root)
    
    # Wait a moment for server to start
    time.sleep(2)

    # 3. Open Frontend
    print("\n[3/3] Opening Dashboard...")
    frontend_html = os.path.join(project_root, "frontend", "index.html")
    file_url = "file://" + os.path.abspath(frontend_html).replace("\\", "/")
    
    print(f"Opening: {file_url}")
    webbrowser.open(file_url)

    print("\n==========================================")
    print("   Server is running at http://127.0.0.1:8000")
    print("   Dashboard is open in your browser.")
    print("   Press Ctrl+C to stop the server.")
    print("==========================================")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server_proc.terminate()
        server_proc.wait()
        print("Done. Have a productive day.")

if __name__ == "__main__":
    main()
