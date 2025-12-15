import os
import sys
import tempfile
import subprocess

from config import RUN_TIMEOUT

# ---------------- EXECUTION ----------------
def run_code(code: str):
    wd = tempfile.mkdtemp()
    path = os.path.join(wd, "main.py")

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        p = subprocess.run(
            [sys.executable, path],
            cwd=wd,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
        )
        return p.returncode, p.stdout, p.stderr, wd

    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT", wd