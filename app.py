"""
NL → Code → Run → Fix + Benchmark
Final cleaned version (nitpicks fixed)
"""

import os
import sys
import tempfile
import subprocess
import time
import glob
import ast
from typing import List, Dict, Any

# ---------------- CPU SAFETY ----------------
CPU_THREADS = 2
os.environ["OMP_NUM_THREADS"] = str(CPU_THREADS)
os.environ["MKL_NUM_THREADS"] = str(CPU_THREADS)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import gradio as gr

# ---------------- CONFIG ----------------
MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B"
FALLBACK_MODEL = "deepseek-ai/deepseek-coder-1.3b-base"
RUN_TIMEOUT = 20
MAX_NEW_TOKENS = 384

# ---------------- BENCHMARK TASKS ----------------
BENCHMARK_TASKS = [
    ("DSA", "Given [1,2,3,4,5] and k=7, print the length of the longest contiguous subarray with sum <= k."),
    ("DSA", "Given s='anagram' and t='nagaram', print True if t is an anagram of s."),
    ("DSA", "Given the string 'leetcode', print the index of the first non-repeating character."),
    ("DSA", "Group the anagrams in ['eat','tea','tan','ate','nat','bat'] and print the result."),
    ("DSA", "Given nums=[2,7,11,15] and target=9, print the two indices."),
    ("Algo", "Given [10,9,2,5,3,7,101,18], print the length of LIS."),
    ("Algo", "Given integer 16, print True if it is a power of two."),
    ("IO", "Create scores.csv with ('Alice',90),('Bob',80),('Alice',70),('Bob',85). Print average score per name."),
    ("Plot", "Plot numbers 1 to 10 vs their squares and save the figure."),
    ("Plot", "Generate 500 random numbers and plot a histogram, save it."),
]

# ---------------- LOAD MODEL ----------------
print(f"Loading model {MODEL_NAME}...", flush=True)
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)
    device = 0 if torch.cuda.is_available() else -1
    model.to("cuda" if device == 0 else "cpu")
    text_gen = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
except Exception:
    tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL)
    model = AutoModelForCausalLM.from_pretrained(FALLBACK_MODEL)
    model.to("cpu")
    text_gen = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# ---------------- PROMPTS ----------------
SYSTEM_PREFIX = (
    "# You are a careful Python coding assistant.\n"
    "# Output runnable Python code only.\n"
    "# Allowed libs: math, itertools, collections, heapq, functools, numpy, pandas, matplotlib.\n"
    "#\n"
    "# STRICT RULES:\n"
    "# - Identify standard DSA patterns when applicable.\n"
    "# - Prefer pure Python for algorithmic problems.\n"
    "# - ONLY generate plots if the task explicitly asks for plotting, charts, graphs, or visualization.\n"
    "# - If plotting is NOT requested, DO NOT import matplotlib and DO NOT generate plots.\n"
    "# - For DSA problems, plotting is strictly forbidden.\n"
    "# - Do NOT use input(). Define all data inline.\n"
)

GEN_PROMPT = (
    SYSTEM_PREFIX
    + "Instruction:\n"
      "Write a single-file Python script that solves the task.\n"
      "Output ONLY runnable Python code.\n\n"
      "Task:\n{task}\n\n"
      "Script:\n"
)

FIX_PROMPT = (
    SYSTEM_PREFIX
    + "Instruction:\n"
      "Fix the following script while preserving correctness.\n\n"
      "Script:\n{code}\n\n"
      "Issue:\n{issue}\n\n"
      "Corrected script:\n"
)

# ---------------- HELPERS ----------------
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
        warnings.append("Plotting code removed because task did not request visualization.")
    return warnings

# ---------------- EXECUTION ----------------
def run_code(code: str):
    wd = tempfile.mkdtemp()
    path = os.path.join(wd, "main.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        p = subprocess.run([sys.executable, path], cwd=wd, capture_output=True, text=True, timeout=RUN_TIMEOUT)
        return p.returncode, p.stdout, p.stderr, wd
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT", wd

# ---------------- CORE TASK ----------------
def run_task(task: str) -> Dict[str, Any]:
    code = text_gen(
        GEN_PROMPT.format(task=task),
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,
        return_full_text=False,
    )[0]["generated_text"].replace("```", "").strip()

    try:
        ast.parse(code)
    except SyntaxError as e:
        code = text_gen(
            FIX_PROMPT.format(code=code, issue=str(e)),
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            return_full_text=False,
        )[0]["generated_text"].replace("```", "").strip()

    rc, out, err, wd = run_code(code)

    warnings = find_warnings(code, task)

    if warnings:
        code = strip_plotting_code(code)
        rc, out, err, wd = run_code(code)

    status = "FAILED"
    if rc == 0:
        status = "SUCCESS" if not warnings else "SUCCESS (with warnings)"

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

# ---------------- BENCHMARK ----------------
def run_benchmark():
    results = []
    for _, task in BENCHMARK_TASKS:
        start = time.time()
        res = run_task(task)
        elapsed = time.time() - start
        results.append((res["status"].startswith("SUCCESS"), elapsed))

    total = len(results)
    success = sum(1 for r, _ in results if r)

    return (
        f"Total tasks: {total}\n"
        f"Eventual success: {100*success/total:.1f}%\n"
        f"Failure rate: {100*(total-success)/total:.1f}%\n"
        f"Average runtime: {sum(t for _, t in results)/total:.2f} s"
    )

# ---------------- UI ----------------
def build_ui():
    with gr.Blocks(title="Generative Coding Agent") as demo:
        gr.Markdown("## Generative Coding Agent (Final Clean Version)")

        task = gr.Textbox(lines=3, label="Task")
        run_btn = gr.Button("Run Task")
        bench_btn = gr.Button("Run Benchmark")

        status = gr.Textbox(label="Status")
        warnings = gr.Textbox(label="Warnings")

        with gr.Accordion("Generated Code", open=True):
            code = gr.Code(lines=20)

        stdout = gr.Textbox(label="STDOUT")
        stderr = gr.Textbox(label="STDERR")
        images = gr.Gallery(label="Images")

        bench_out = gr.Textbox(label="Benchmark Results", lines=6, visible=False)

        run_btn.click(
            lambda t: (
                lambda r: (r["status"], r["warnings"], r["code"], r["stdout"], r["stderr"], r["images"], "")
            )(run_task(t)),
            [task],
            [status, warnings, code, stdout, stderr, images, bench_out],
        )

        bench_btn.click(
            lambda: ("", "", "", "", "", [], run_benchmark()),
            [],
            [status, warnings, code, stdout, stderr, images, bench_out],
        ).then(
            lambda: gr.update(visible=True),
            [],
            bench_out,
        )

    return demo

if __name__ == "__main__":
    build_ui().launch(share=True)
