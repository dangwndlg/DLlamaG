import os

API_HOST: str = os.getenv("DLLAMAG_API_HOST", "http://ec2-63-34-20-174.eu-west-1.compute.amazonaws.com:8000")
API_VERSION: str = os.getenv("DLLAMAG_API_VERSION", "v1")

MAX_SEQ_LEN: int = 8