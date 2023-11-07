from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from server import api
from server import config as CONF
from server.exceptions import BaseException
from server.models import database, init_db

if CONF.APP_KEY == CONF.DEFAULT_APP_KEY:
    logger.warning(
        f"Default app_key({CONF.APP_KEY}) is not safe, please change it in config.py or env"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()
    await init_db()
    yield
    if database.is_connected:
        await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(api.router)
app.mount("/assets", StaticFiles(directory=CONF.DIST_DIR / "assets"), name="assets")
app.mount("/static", StaticFiles(directory=CONF.DIST_DIR / "static"), name="static")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3333", "http://127.0.0.1:3333"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BaseException)
def handle_base_exception(request: Request, exc: BaseException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(AssertionError)
def handle_assertion_error(request: Request, exc: AssertionError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
