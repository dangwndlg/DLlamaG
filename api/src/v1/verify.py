from config import MAX_SEQ_LEN
from exceptions import DialogException

from typing import Dict, List, Tuple
from custom_types import DLlamaGDialog

ALLOWED_STARTING_ROLES: Tuple[str] = ("system", "user", "assistant")
ALLOWED_ROLES: Tuple[str] = ("user", "assistant")

async def verify_dialogs(dialogs: List[DLlamaGDialog]) -> Dict[str, str]:
    # Verify dialogs are of correct length
    n: int = len(dialogs)
    if n > MAX_SEQ_LEN:
        raise DialogException(f"Dialogs length cannot exceed {MAX_SEQ_LEN}")
    elif n < 1:
        raise DialogException("Must have at least one user dialog")
    
    # Verify roles of first and last dialog
    if dialogs[0].role not in ALLOWED_STARTING_ROLES:
        raise DialogException(f"Role for first dialog must be one of {ALLOWED_STARTING_ROLES}")
    elif dialogs[-1].role != "user":
        raise DialogException("Role of final dialog must be 'user'")
    # Unwrap dialogs into form model can take
    verified: List[Dict[str, str]] = [dict(dialogs[0])]

    for d in dialogs[1:]:
        if d.role not in ALLOWED_ROLES:
            raise DialogException(f"After first dialog, role for dialogs must be one of {ALLOWED_ROLES}")
        elif d.role == verified[-1]["role"]:
            raise DialogException("After first dialog, roles must alternate between 'user' and 'assistant'")
        verified.append(dict(d))

    return verified