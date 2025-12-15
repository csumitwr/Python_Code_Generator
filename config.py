import os

# ---------------- CPU SAFETY ----------------
CPU_THREADS = 2
os.environ["OMP_NUM_THREADS"] = str(CPU_THREADS)
os.environ["MKL_NUM_THREADS"] = str(CPU_THREADS)

# ---------------- CONFIG ----------------
MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B"
FALLBACK_MODEL = "deepseek-ai/deepseek-coder-1.3b-base"
RUN_TIMEOUT = 20
MAX_NEW_TOKENS = 384