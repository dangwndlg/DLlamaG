from config import BUILD_LLAMA, LLAMA_CKPT_DIR, LLAMA_TOKENIZER_PATH, IS_DOMINO_ENV

from chat.dlg_llama import DLlamaG

dan: DLlamaG = DLlamaG(
    ckpt_dir=LLAMA_CKPT_DIR,
    tokenizer_path=LLAMA_TOKENIZER_PATH,
    build=BUILD_LLAMA
)

def dummy_dan_response(prompt: str) -> str:
    history = [[{
        "role": "user",
        "content": prompt
    }]]
    
    if IS_DOMINO_ENV:
        return dan.chat_complete(history).response

    response = dan.dummy_chat_complete(history)
    return response.response