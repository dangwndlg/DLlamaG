from fastapi import FastAPI
import uvicorn

from app import create_app
from config import API_HOST, API_PORT

def main() -> None:
    app: FastAPI = create_app()

    uvicorn.run(app=app, host=API_HOST, port=API_PORT)
    
if __name__ == "__main__":
    main()