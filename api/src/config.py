import os

API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", 8000))

BUILD_LLAMA: bool = True if os.getenv("BUILD_LLAMA", "").lower() == "true" else False

LLAMA_CKPT_DIR: str = ""
LLAMA_TOKENIZER_PATH: str = ""

MAX_SEQ_LEN: int = 8