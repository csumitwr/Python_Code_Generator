import gradio as gr

from tasks import run_task
from benchmark import run_benchmark

# ---------------- UI ----------------

def build_ui(text_gen):
    """
        Builds and returns the Gradio UI.
        The model pipeline is injected via `text_gen`.
    """

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

        bench_out = gr.Textbox(
            label="Benchmark Results",
            lines=6,
            visible=False,
        )

        run_btn.click(
            lambda t: (
                lambda r: (
                    r["status"],
                    r["warnings"],
                    r["code"],
                    r["stdout"],
                    r["stderr"],
                    r["images"],
                    "",
                )
            )(run_task(t, text_gen)),
            [task],
            [status, warnings, code, stdout, stderr, images, bench_out],
        )

        bench_btn.click(
            lambda: ("", "", "", "", "", [], run_benchmark(text_gen)),
            [],
            [status, warnings, code, stdout, stderr, images, bench_out],
        ).then(
            lambda: gr.update(visible=True),
            [],
            bench_out,
        )

    return demo