"""FastAPI application: serves the chat page and the streaming chat API."""
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from personality import build_system_prompt

load_dotenv()

# Logging: INFO level to stdout, includes timestamps and logger names.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("ktulue.web")

STATIC_DIR = Path(__file__).parent / "static"

# Mutable state populated either by lifespan (production) or by tests directly.
state: dict = {"system_prompt": None, "client": None}

# Module-level session store. Tests reset this via the conftest fixture.
sessions: dict[str, list[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the system prompt and Anthropic client once at startup."""
    logger.info("Building system prompt...")
    state["system_prompt"] = build_system_prompt()
    logger.info("System prompt ready.")
    state["client"] = anthropic.Anthropic()
    logger.info("Anthropic client ready.")
    yield


app = FastAPI(title="KtulueBot Web", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serve the chat page."""
    return FileResponse(STATIC_DIR / "index.html")
