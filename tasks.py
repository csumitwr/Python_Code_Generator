import ast
import glob
import os
from typing import Dict, Any, List

from prompts import GEN_PROMPT, FIX_PROMPT
from execution import run_code
from config import MAX_NEW_TOKENS

# ---------------- CORE TASK ----------------

def task_requests_plot(task: str) -> bool:
    keywords = ["plot", "graph", "chart", "visualize", "histogram"]
    return any(k in task.lower() for k in keywords)


def strip_plotting_code(code: str) -> str:
    cleaned = []
    for line in code.splitlines():
        s = line.strip()
        if s.startswith("import matplotlib") or s.startswith("from matplotlib"):
            continue
        if "plt." in s:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def find_warnings(code: str, task: str) -> List[str]:
    warnings = []
    if not task_requests_plot(task) and ("matplotlib" in code or "plt." in code):
        warnings.append(
            "Plotting code removed because task did not request visualization."
        )
    return warnings


def run_task(task: str, text_gen) -> Dict[str, Any]:
    """
    Runs a single NL → Code → Run → Fix cycle.
    """

    # -------- Code generation --------

    code = text_gen(
        GEN_PROMPT.format(task=task),
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,
        return_full_text=False,
    )[0]["generated_text"].replace("```", "").strip()

    # -------- Syntax validation --------

    try:
        ast.parse(code)
    except SyntaxError as e:
        code = text_gen(
            FIX_PROMPT.format(code=code, issue=str(e)),
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            return_full_text=False,
        )[0]["generated_text"].replace("```", "").strip()

    # -------- Execute --------

    rc, out, err, wd = run_code(code)

    # -------- Plot guardrails --------

    warnings = find_warnings(code, task)
    if warnings:
        code = strip_plotting_code(code)
        rc, out, err, wd = run_code(code)

    # -------- Status --------

    status = "FAILED"
    if rc == 0:
        status = "SUCCESS" if not warnings else "SUCCESS (with warnings)"

    # -------- Collect artifacts --------
    
    images = []
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        images.extend(glob.glob(os.path.join(wd, ext)))

    return {
        "status": status,
        "warnings": "\n".join(warnings),
        "code": code,
        "stdout": out,
        "stderr": err,
        "images": images,
    }