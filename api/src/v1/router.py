from fastapi import APIRouter, HTTPException, status

from config import BUILD_LLAMA, LLAMA_CKPT_DIR, LLAMA_TOKENIZER_PATH
from exceptions import DialogException
from v1.bot import ChatBot
from v1.verify import verify_dialogs

from typing import Dict, List
from custom_types import ChatCompleteFunction, DLlamaGResponse, DialogList

v1_router: APIRouter = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

dan: ChatBot = ChatBot(
    ckpt_dir=LLAMA_CKPT_DIR,
    tokenizer_path=LLAMA_TOKENIZER_PATH,
    build=BUILD_LLAMA
)
chat_complete: ChatCompleteFunction = dan.chat_complete if BUILD_LLAMA else dan.dummy_chat_complete

@v1_router.get("/health")
async def health_check():
    return {"success": True}

@v1_router.post("/chat")
async def chat(data: DialogList) -> DLlamaGResponse:
    try:
        verified: List[Dict[str,str]] = await verify_dialogs(dialogs=data.dialogs)
        print(await chat_complete([verified]))
    except DialogException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    
    print(verified)
    
    return DLlamaGResponse(
        last_message="",
        response=""
    )