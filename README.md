🧠 Generative Python Coding Agent:

A modular NL → Code → Run → Fix generative coding agent that converts natural language tasks into executable Python code, runs them safely, auto-fixes errors, and reports results through a Gradio UI.
Designed with strict execution guardrails, deterministic generation, and a clean separation of concerns.

✨ What this project does:
1. Converts natural language tasks → runnable Python scripts
2. Executes code in a sandboxed subprocess with timeouts
3. Automatically fixes syntax errors using model feedback
4. Enforces plotting guardrails (no plots unless explicitly requested)
5. Collects stdout, stderr, and generated artifacts
6. Provides a live Gradio UI
7. Includes a built-in benchmark suite

🧩 Project Structure:

The project is modular by design: app.py is the entry point that loads the model once and launches the UI, while config.py centralizes safety limits and global settings. model.py handles isolated model loading, prompts.py stores fixed prompt templates, and execution.py runs generated code in a sandboxed environment. The core agent logic lives in tasks.py, which converts natural language into code, executes it, and fixes errors iteratively, while benchmark.py evaluates performance on coding benchmarks. Finally, ui.py exposes everything through a clean Gradio interface.

⚙️ Requirements:

Python 3.10+ (recommended: 3.10 or 3.11)
Internet connection (first run downloads model weights)

How to run: 

Open app.py in any IDE or Terminal and run the file (after creating a virtual invironment and installing all the packages listed in requirments.txt).

Python packages: Core dependencies:

1. torch
2. transformers
3. gradio

Optional (used by generated code, not the app itself):

1. numpy
2. pandas
3. matplotlib

Install dependencies: 

pip install torch transformers gradio

🖥️ Using the App:

Run Task:
Enter a natural language task
Click Run Task
View:
1. Status
2. Generated code
3. STDOUT / STDERR
4. Images (if any)
    
OR
  
Click Run Benchmark
1. Click Run Benchmark
2. Executes a predefined suite of tasks

Displays:

1. Total tasks
2. Eventual success rate
3. Failure rate
4. Average runtime

🔒 Safety & Guardrails:

1. Timeout-bounded execution
2. Restricted imports
3. No runtime package installation
4. Plotting forbidden unless explicitly requested
5. Pure Python preferred for algorithmic tasks
6. No input() usage allowed

🧠 Models:

Default model:
Qwen/Qwen2.5-Coder-1.5B

Fallback:

deepseek-ai/deepseek-coder-1.3b-base
