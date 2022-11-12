import os
import argparse

import uvicorn
from fastapi.responses import HTMLResponse, RedirectResponse
from loguru import logger

from server import app
from server import config as CONF


@app.get("/", response_class=RedirectResponse)
async def index():
    with open(CONF.DIST_DIR / "index.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/home", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/")


# Avoid lost router when refreshing on preview page
@app.get("/preview", response_class=HTMLResponse)
async def preview():
    return RedirectResponse(url="/")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()

    if not os.getenv("APPKEY"):
        os.environ["APPKEY"] = "1234567890"
        logger.warning(f"APPKEY not set, using default {os.getenv('APPKEY')}")

    uvicorn.run(app="server:app",
                host=args.bind,
                port=args.port,
                reload=bool(os.getenv("DEBUG")))
