from fastapi import FastAPI

from v1.router import v1_router

def create_app(*args, **kwargs) -> FastAPI:
    """
    Creates a FastAPI app which includes the API routes

    @returns FastAPI: App
    """
    app: FastAPI = FastAPI(*args, **kwargs)

    app.include_router(v1_router)

    return app