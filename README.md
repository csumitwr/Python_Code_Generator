🧠 Generative Python Coding Agent

A natural-language → code → run → fix Python agent that safely generates, executes, and auto-corrects code using a local LLM. It’s modular, deterministic, and designed with strict execution guardrails, exposed through a lightweight Gradio UI.

✨ What it does

Takes plain-English tasks, turns them into runnable Python, executes them in a sandbox with timeouts, fixes errors iteratively using model feedback, captures stdout/stderr/files, enforces no-plot rules unless requested, and includes a built-in benchmark runner.

🧩 Architecture

app.py boots the model and UI, tasks.py handles NL→code→execute→fix loops, execution.py sandboxes code, prompts.py stores fixed prompts, config.py defines safety limits, benchmark.py runs evaluations, and ui.py exposes everything via Gradio.

⚙️ Requirements & Run

Requires Python 3.10+ and internet on first run to download model weights. Create a virtual env, install torch, transformers, and gradio, then run python app.py.

🖥️ Usage

Use Run Task to execute natural-language instructions and inspect generated code, logs, and outputs, or Run Benchmark to evaluate success rate, failures, and runtime across predefined tasks.

🔒 Safety

Execution is timeout-bounded, imports are restricted, package installs are blocked, input() is disallowed, and plotting is forbidden unless explicitly requested to keep runs deterministic and safe.

🧠 Models

Default model is Qwen/Qwen2.5-Coder-1.5B, with DeepSeek-Coder-1.3B as a fallback.
