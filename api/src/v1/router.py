from fastapi import APIRouter, HTTPException, Request, status
from uuid import uuid4

from config import (
    BUILD_LLAMA, 
    ENABLE_LOGGING,
    LLAMA_CKPT_DIR, 
    LLAMA_TOKENIZER_PATH,
    LLAMA_TOP_P,
    LLAMA_MAX_BATCH_SIZE,
    LLAMA_MAX_SEQ_LEN,
    LLAMA_MAX_GEN_LEN,
    LLAMA_TEMPERATURE,
    LOGGING_FILE_NAME,
    LOGGING_DIR
)
from exceptions import DialogException
from logger import JSONLogger
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
    top_p=LLAMA_TOP_P,
    max_batch_size=LLAMA_MAX_BATCH_SIZE,
    max_seq_len=LLAMA_MAX_SEQ_LEN,
    max_gen_len=LLAMA_MAX_GEN_LEN,
    temperature=LLAMA_TEMPERATURE,
    build=BUILD_LLAMA
)
chat_complete: ChatCompleteFunction = dan.chat_complete if BUILD_LLAMA else dan.dummy_chat_complete

v1_logger: JSONLogger = JSONLogger(
    log_file_name=LOGGING_FILE_NAME,
    log_dir=LOGGING_DIR
)

@v1_router.get("/health")
async def health_check(request: Request):
    """
    Health check endpoint for v1 router
    """
    request_id: str = str(uuid4())
    if ENABLE_LOGGING:
        await v1_logger.log_incoming_request(
            request_id=request_id,
            request_type="health",
            request=request
        )
    return {"success": True}

@v1_router.post("/chat")
async def chat(data: DialogList, request: Request) -> DLlamaGResponse:
    """
    Chat endpoint for v1 router
    Request body:
        {
            dialogs: [
                {
                    role: string,
                    content: string
                },
                ...
            ]
        }
    Response body:
        {
            last_message: string,
            response: string
        }
    """
    request_id: str = str(uuid4())
    
    if ENABLE_LOGGING:
        await v1_logger.log_incoming_request(
            request_id=request_id,
            request_type="chat",
            request=request
        )
    
    try:
        verified: List[Dict[str,str]] = await verify_dialogs(dialogs=data.dialogs)
        chat_response: DLlamaGResponse = await chat_complete(verified)
        if ENABLE_LOGGING:
            await v1_logger.log_outgoing_response(
                request_id=request_id,
                request_type="chat",
                outgoing_response=dict(chat_response)
            )
        return chat_response
    except DialogException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
