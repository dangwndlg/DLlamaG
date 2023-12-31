from config import LLAMA_MAX_BATCH_SIZE
from exceptions import DialogException

from typing import Dict, List, Tuple
from custom_types import DLlamaGDialog

ALLOWED_STARTING_ROLES: Tuple[str] = ("system", "user")
ALLOWED_ROLES: Tuple[str] = ("user", "assistant")

async def verify_dialogs(dialogs: List[DLlamaGDialog]) -> List[Dict[str, str]]:
    """
    Verifies whether a list of dialogs is valid, and converts them into a 
        dictionary to be processed by the LLaMA model

    @param List[DLlamaGDialog] dialogs: List of dialogs to verify

    @returns List[Dict[str, str]]: "jsonified" dialogs
    """
    # Verify dialogs are of correct length
    n: int = len(dialogs)
    if n > LLAMA_MAX_BATCH_SIZE:
        raise DialogException(f"Dialogs length cannot exceed {LLAMA_MAX_BATCH_SIZE}")
    elif n < 1:
        raise DialogException("Must have at least one user dialog")
    
    # Verify roles of first and last dialog
    if dialogs[0].role not in ALLOWED_STARTING_ROLES:
        raise DialogException(f"Role for first dialog must be one of {ALLOWED_STARTING_ROLES}")
    elif dialogs[-1].role != "user":
        raise DialogException("Role of final dialog must be 'user'")
    elif n > 1 and dialogs[0].role == "system" and dialogs[1].role != "user":
        raise DialogException("Dialog roles must be sequenced (s/)u/a/u/a/.../u")
    # Unwrap dialogs into form model can take
    verified: List[Dict[str, str]] = [dict(dialogs[0])]

    # Verify dialogs sequentially and add them to the list of verified
    for d in dialogs[1:]:
        if d.role not in ALLOWED_ROLES:
            raise DialogException(f"After first dialog, role for dialogs must be one of {ALLOWED_ROLES}")
        elif d.role == verified[-1]["role"]:
            raise DialogException("Dialog roles must be sequenced (s/)u/a/u/a/.../u")
        verified.append(dict(d))

    return verified