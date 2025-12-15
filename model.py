import torch

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import MODEL_NAME, FALLBACK_MODEL

# ---------------- LOAD MODEL ----------------

def load_text_generator():
    """ 
        Loads and returns a HuggingFace text-generation pipeline.
        Model loading happens ONLY when this function is called.
    """

    print(f"Loading model {MODEL_NAME}...", flush=True)

    try:
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        )

        device = 0 if torch.cuda.is_available() else -1
        model.to("cuda" if device == 0 else "cpu")
        return pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device,
        )

    except Exception:
        print("Primary model failed, loading fallback...", flush=True)
        tokenizer = AutoTokenizer.from_pretrained(FALLBACK_MODEL)
        model = AutoModelForCausalLM.from_pretrained(FALLBACK_MODEL)
        model.to("cpu")

        return pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1,
        )