import os

IS_DOMINO_ENV: bool = True if os.getenv("DOMINO_NODE_IP") else False