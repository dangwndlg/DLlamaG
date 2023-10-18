from fastapi import APIRouter, HTTPException, Request, status

from config import (
    BUILD_LLAMA, 
    LLAMA_CKPT_DIR, 
    LLAMA_TOKENIZER_PATH,
    LLAMA_TOP_P,
    LLAMA_MAX_BATCH_SIZE,
    LLAMA_MAX_SEQ_LEN,
    LLAMA_MAX_GEN_LEN,
    LLAMA_TEMPERATURE
)
from exceptions import DialogException
from v1.bot import ChatBot
from v1.verify import verify_dialogs

from typing import Any, Dict, List
from custom_types import ChatCompleteFunction, DLlamaGResponse, DialogList

v1_router: APIRouter = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

dan: ChatBot = ChatBot(
    ckpt_dir=LLAMA_CKPT_DIR,
    tokenizer_path=LLAMA_TOKENIZER_PATH,
    top_p=LLAMA_TOP_P,
    max_batch_size=LLAMA_MAX_BATCH_SIZE,
    max_seq_len=LLAMA_MAX_SEQ_LEN,
    max_gen_len=LLAMA_MAX_GEN_LEN,
    temperature=LLAMA_TEMPERATURE,
    build=BUILD_LLAMA
)
chat_complete: ChatCompleteFunction = dan.chat_complete if BUILD_LLAMA else dan.dummy_chat_complete

@v1_router.get("/health")
async def health_check(request: Request):
    print(request.client)
    return {"success": True}

@v1_router.post("/chat")
async def chat(data: DialogList, request: Request) -> DLlamaGResponse:
    logging_data: Dict[str, Any] = {
        "origin": {
            "host": request.client.host,
            "port": request.client.port
        },
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "chat_history": await request.body()
    }
    print(logging_data)
    try:
        verified: List[Dict[str,str]] = await verify_dialogs(dialogs=data.dialogs)
        return await chat_complete(verified)
    except DialogException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )