import argparse
import os

import uvicorn
from fastapi import Request
from fastapi.responses import HTMLResponse

from server import app
from server import config as CONF

with open(CONF.DIST_DIR / "index.html") as f:
    index_page = HTMLResponse(content=f.read())


@app.middleware("http")
async def redirect(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return index_page
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()

    uvicorn.run(app="main:app", host=args.bind, port=args.port, reload=bool(os.getenv("DEBUG")))
