import os

API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", 8000))

BUILD_LLAMA: bool = True if os.getenv("BUILD_LLAMA", "").lower() == "true" else False

LLAMA_CKPT_DIR: str = os.getenv("LLAMA_CKPT_DIR", "")
LLAMA_TOKENIZER_PATH: str = os.getenv("LLAMA_TOKENIZER_PATH", "")

MAX_SEQ_LEN: int = 8