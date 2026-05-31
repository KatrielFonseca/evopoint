import subprocess
import time
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

backend_path = os.path.join(
    BASE_DIR,
    "backend.exe"
)

frontend_path = os.path.join(
    BASE_DIR,
    "frontend.exe"
)

subprocess.Popen(
    backend_path,
    creationflags=subprocess.CREATE_NO_WINDOW
)

time.sleep(5)

subprocess.Popen(
    frontend_path
)