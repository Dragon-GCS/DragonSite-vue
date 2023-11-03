import argparse
import os

import uvicorn
from loguru import logger

if not os.getenv("APP_KEY"):
    os.environ["APP_KEY"] = "1234567890"
    logger.warning(f"APP_KEY not set, using default {os.getenv('APP_KEY')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()
    uvicorn.run(app="server:app", host=args.bind, port=args.port, reload=bool(os.getenv("DEBUG")))
