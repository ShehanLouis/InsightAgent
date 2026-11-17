import os
import sys
import subprocess

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    
    # Virtual environment python if available
    venv_python = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    print("=" * 65)
    print("  InsightAgent | Autonomous AI Data Analyst & Decision Platform")
    print("=" * 65)
    print(f"[*] Python Executable: {python_exe}")
    print(f"[*] Backend Directory: {backend_dir}")
    print("[*] Launching FastAPI + Embedded Dashboard at: http://127.0.0.1:8000")
    print("[*] API Documentation (Swagger) at:        http://127.0.0.1:8000/docs")
    print("=" * 65)
    print("Press Ctrl+C to stop the server.\n")

    cmd = [python_exe, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
    subprocess.run(cmd, cwd=backend_dir)

if __name__ == "__main__":
    main()
