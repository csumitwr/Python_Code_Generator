from model import load_text_generator
from ui import build_ui

# ---------------- ENTRY POINT ----------------

def main():
    text_gen = load_text_generator()
    demo = build_ui(text_gen)
    demo.launch(share=True)


if __name__ == "__main__":
    main()