from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server import api
from server import config as CONF
from server.models import database, init_db

app = FastAPI()
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


@app.on_event("startup")
async def connect_db():
    if not database.is_connected:
        await database.connect()
    await init_db()


@app.on_event("shutdown")
async def disconnect_db():
    if database.is_connected:
        await database.disconnect()

