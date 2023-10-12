from fastapi import FastAPI

from v1.router import v1_router

def create_app(*args, **kwargs) -> FastAPI:
    app: FastAPI = FastAPI(*args, **kwargs)

    app.include_router(v1_router)

    return app