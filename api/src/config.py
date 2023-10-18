import os

API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", 8000))

ENABLE_LOGGING: bool = False
LOGGING_LOC: str = ""

# Whether to build the full llama model or test dummy
BUILD_LLAMA: bool = True if os.getenv("BUILD_LLAMA", "").lower() == "true" else False

# Path to the model checkpoints (e.g. .../llama-chat-2-7b)
LLAMA_CKPT_DIR: str = os.getenv("LLAMA_CKPT_DIR", "")
# Path to model tokenizer (e.g. .../tokenizer.model) 
LLAMA_TOKENIZER_PATH: str = os.getenv("LLAMA_TOKENIZER_PATH", "")

# Top-p probability threshold for nucleus sampling
LLAMA_TOP_P: float = float(os.getenv("LLAMA_TOP_P", 0.9))
# Maximum batch size for inference
LLAMA_MAX_BATCH_SIZE: int = int(os.getenv("LLAMA_MAX_BATCH_SIZE", 10))
# Maximum sequence length for input text
LLAMA_MAX_SEQ_LEN: int = int(os.getenv("LLAMA_MAX_SEQ_LEN", 1024))
# Maximum length of the generated text sequence
LLAMA_MAX_GEN_LEN: int = int(os.getenv("LLAMA_MAX_GEN_LEN", LLAMA_MAX_SEQ_LEN/4))
# Temperature value for controlling randomness in sampling
LLAMA_TEMPERATURE: float = float(os.getenv("LLAMA_TEMPERATURE", 0.6))