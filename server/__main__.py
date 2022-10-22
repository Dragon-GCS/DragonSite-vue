import os
import argparse

import uvicorn
from loguru import logger


if not os.getenv("APPKEY"):
    os.environ["APPKEY"] = "1234567890"
    logger.warning(f"APPKEY not set, using default {os.getenv('APPKEY')}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()
    uvicorn.run(app="server:app",
                host=args.bind,
                port=args.port,
                reload=bool(os.getenv("DEBUG")))
