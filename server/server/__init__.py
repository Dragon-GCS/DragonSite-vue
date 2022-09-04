from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from server import api
from server import config as CONF
from server.models import database, init_db

app = FastAPI()
app.include_router(api.router)
app.mount("/assets", StaticFiles(directory=CONF.DIST_DIR / "assets"), name="assets")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def connect_db():
    await init_db()
    await database.connect()


@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()


@app.get("/", response_class=RedirectResponse)
async def index():
    return RedirectResponse(url="/home")


@app.get("/home", response_class=HTMLResponse)
async def home():
    with open(CONF.DIST_DIR / "index.html") as f:
        return HTMLResponse(content=f.read())
