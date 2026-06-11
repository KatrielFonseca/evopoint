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
# EXECUTÁVEIS
# =========================================

backend_path = os.path.join(
    BASE_DIR,
    "AVAPointAPI.exe"
)

frontend_path = os.path.join(
    BASE_DIR,
    "AVAPoint.exe"
)

# =========================================
# VALIDAÇÃO
# =========================================

if not os.path.exists(backend_path):

    raise Exception(

        f"Backend não encontrado:\n\n{backend_path}"

    )

if not os.path.exists(frontend_path):

    raise Exception(

        f"Frontend não encontrado:\n\n{frontend_path}"

    )

# =========================================
# INICIA BACKEND
# =========================================

subprocess.Popen(

    backend_path,

    creationflags=subprocess.CREATE_NO_WINDOW

)

# =========================================
# AGUARDA API
# =========================================

api_online = False

for _ in range(30):

    try:

        response = requests.get(

            "http://127.0.0.1:8000/",

            timeout=2

        )

        if response.status_code == 200:

            api_online = True

            break

    except:

        pass

    time.sleep(1)

# =========================================
# INICIA FRONTEND
# =========================================

if api_online:

    subprocess.Popen(

        frontend_path

    )

else:

    raise Exception(

        "AVAPoint API não iniciou."

    )