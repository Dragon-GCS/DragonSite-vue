import uvicorn
import os

from loguru import logger

if not os.getenv("APPKEY"):
    os.environ["APPKEY"] = "1234567890"
    logger.warning(f"APPKEY not set, using default {os.getenv('APPKEY')}")

if __name__ == '__main__':
    uvicorn.run(app="server:app",
                host="0.0.0.0",
                port=8080,
                reload=bool(os.getenv("DEBUG")))
