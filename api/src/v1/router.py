from fastapi import APIRouter, HTTPException, status

from exceptions import DialogException
from v1.verify import verify_dialogs

from typing import Dict, List
from custom_types import DLlamaGResponse, DialogList

v1_router: APIRouter = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

@v1_router.get("/health")
async def health_check():
    return {"success": True}

@v1_router.post("/chat")
async def chat(data: DialogList) -> DLlamaGResponse:
    try:
        verified: List[Dict[str,str]] = await verify_dialogs(dialogs=data.dialogs)
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