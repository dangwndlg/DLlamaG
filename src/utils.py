from flask import request

def get_current_domino_user() -> str:
    return request.headers.get("domino-username", "UNKNOWN")