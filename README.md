**NL → Code → Run → Fix + Benchmark**

Overview: 
This notebook implements a reasoning-aware generative coding agent that converts natural-language programming tasks into runnable Python code, executes it in a sandbox, automatically fixes errors, and evaluates performance using a built-in benchmark. The system is designed to demonstrate agentic reasoning, not just code generation.

What This Does:
1. Takes a plain-English coding task
2. Generates Python code only (no markdown, no explanations)
3. Executes the code safely with timeouts
4. Automatically retries on failure using error feedback
5. Enforces strict rules (no installs, no plotting unless requested)
6. Runs a benchmark to measure model quality

Key Features:
1. ✅ Auto-fix loop (generate → run → fix)
2. 🛡️ Guardrails against unsafe code
3. 📊 One-click benchmark dashboard
4. 🧠 DSA-aware prompt enforcement
5. 🖼️ Plotting allowed only when explicitly requested

**How to Run (Kaggle)**
Install dependencies:
!pip install -q torch transformers accelerate sentencepiece gradio

Run the app:
!python app.py

Benchmark Metrics:
1. Total tasks
2. Success rate
3. Failure rate
4. Average runtime
These help compare prompt-engineered models vs stock models.

Example Tasks:
“Given nums=[1,2,3,-2,2] and target=3, print the number of subarrays.”
“Check if two strings are anagrams.”
“Group anagrams in a list.”
“Plot x vs x² and save the figure.”
