import os


IS_DOMINO_ENV: bool = bool(os.getenv("DOMINO_NODE_IP"))
BUILD_LLAMA: bool = IS_DOMINO_ENV

LLAMA_CKPT_DIR: str = os.getenv("LLAMA_CKPT_DIR", "")
LLAMA_TOKENIZER_PATH: str = os.getenv("LLAMA_TOKENIZER_PATH", "")

UNKNOWN: str = "UNKNOWN"