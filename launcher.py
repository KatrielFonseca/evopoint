import subprocess
import time
import os
import sys
import requests

# =========================================
# BASE DIR
# =========================================

if getattr(sys, "frozen", False):

    BASE_DIR = os.path.dirname(
        sys.executable
    )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

# =========================================
# PATHS
# =========================================

backend_path = os.path.join(
    BASE_DIR,
    "EVOPointAPI.exe"
)

frontend_path = os.path.join(
    BASE_DIR,
    "EVOPoint.exe"
)

# =========================================
# CHECK FILES
# =========================================

if not os.path.exists(backend_path):

    raise Exception(
        f"Backend não encontrado:\n{backend_path}"
    )

if not os.path.exists(frontend_path):

    raise Exception(
        f"Frontend não encontrado:\n{frontend_path}"
    )

# =========================================
# START BACKEND
# =========================================

subprocess.Popen(
    backend_path,
    creationflags=subprocess.CREATE_NO_WINDOW
)

# =========================================
# WAIT API
# =========================================

api_online = False

for _ in range(30):

    try:

        requests.get(
            "http://127.0.0.1:8000/settings/version",
            timeout=2
        )

        api_online = True

        break

    except:

        time.sleep(1)

# =========================================
# START FRONTEND
# =========================================

if api_online:

    subprocess.Popen(
        frontend_path
    )

else:

    raise Exception(
        "API não iniciou."
    )