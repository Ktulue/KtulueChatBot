"""FastAPI application: serves the chat page and the streaming chat API."""
import json
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from personality import build_system_prompt
from web.errors import pick_friendly_error

load_dotenv()

# Logging: INFO level to stdout, includes timestamps and logger names.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("ktulue.web")

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024

STATIC_DIR = Path(__file__).parent / "static"

# Mutable state populated either by lifespan (production) or by tests directly.
state: dict = {"system_prompt": None, "client": None}

# Module-level session store. Tests reset this via the conftest fixture.
sessions: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the system prompt and Anthropic client once at startup."""
    logger.info("Building system prompt...")
    state["system_prompt"] = build_system_prompt()
    logger.info("System prompt ready.")
    state["client"] = anthropic.Anthropic()
    logger.info("Anthropic client ready.")
    yield
    if state["client"] is not None:
        state["client"].close()


app = FastAPI(title="KtulueBot Web", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def stream_claude_tokens(history: list[dict]):
    """Yield text tokens from Claude's streaming API.

    Pulled out as a separate function so tests can patch it without mocking
    the entire Anthropic SDK surface.
    """
    client = state["client"]
    system_prompt = state["system_prompt"]
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=history,
    ) as response:
        for text in response.text_stream:
            yield text


def _sse_event(event_type: str, text: str) -> str:
    """Format a single Server-Sent Events `data:` line."""
    payload = json.dumps({"type": event_type, "text": text})
    return f"data: {payload}\n\n"


@app.get("/")
async def root():
    """Serve the chat page."""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Stream a chat response token-by-token via Server-Sent Events."""
    session_id = req.session_id
    user_message = req.message

    history = sessions.setdefault(session_id, [])
    history.append({"role": "user", "content": user_message})
    logger.info("[%s] user: %s", session_id, user_message)

    def event_generator():
        collected: list[str] = []
        for token in stream_claude_tokens(history):
            collected.append(token)
            yield _sse_event("token", token)

        full_response = "".join(collected)
        history.append({"role": "assistant", "content": full_response})
        logger.info("[%s] bot: %s", session_id, full_response)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
