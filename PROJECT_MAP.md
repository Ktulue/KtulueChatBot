# Project Map

Living navigation guide for the KtulueChatBot codebase. Updated as the project evolves.

## Core Files

| File | What It Does |
|------|-------------|
| `main.py` | Entry point. Runs the conversation loop, handles user input, calls Claude API. Run with `python main.py`. |
| `personality.py` | Builds the system prompt by reading knowledge files and combining them with voice directives and guardrails. |
| `deflections.py` | Three pools of pre-written deflection responses (humor, redirect, Water Father). Used as examples in the system prompt. |
| `github_client.py` | Fetches recent public repos from GitHub API for dynamic project knowledge. |

## Web Layer

All in the `web/` directory. Wraps the CLI bot in a FastAPI app with a streaming chat endpoint and a static frontend.

| File | What It Does |
|------|-------------|
| `web/app.py` | FastAPI application. Serves the chat page, mounts static files, and exposes `POST /api/chat` as a Server-Sent Events stream. Uses the same `personality.build_system_prompt()` as the CLI. |
| `web/errors.py` | In-character friendly error message pool shown to visitors when something fails server-side. |
| `web/static/index.html` | The chat page markup: header, message area, input, footer disclosure. |
| `web/static/styles.css` | Dark Ktulue-themed styling matching the landing page. |
| `web/static/chat.js` | Vanilla JavaScript: per-tab session UUID, sending messages, parsing the SSE stream, typing indicator, and friendly error handling. |
| `web/static/logo.png` | Copy of the landing page logo for visual consistency. |

Run with `uvicorn web.app:app --reload` and open `http://localhost:8000`.

## Knowledge Files

All in the `knowledge/` directory. These are markdown files that feed into the system prompt. Edit these to change what the bot knows.

| File | Content |
|------|---------|
| `knowledge/bio.md` | Who Josh is — identity, interests, philosophy, Wicket, plants |
| `knowledge/streaming.md` | Software Saturdays, The Pond, hydration advocacy, socials |
| `knowledge/projects.md` | Hype Control origin story, KtulueChatBot, other projects |
| `knowledge/tech.md` | AI views, industry experience, learning journey, tech stack |
| `knowledge/boundaries.md` | No-go zones — what the bot must never share or discuss |

## Tests

All in the `tests/` directory. Run with `pytest`.

| File | Tests |
|------|-------|
| `tests/test_deflections.py` | Deflection pools have enough entries, no duplicates, random selection works |
| `tests/test_github_client.py` | Repo fetching, filtering old repos, API failure handling, prompt formatting |
| `tests/test_personality.py` | System prompt contains all knowledge sections, voice directives, guardrails |
| `tests/test_main.py` | Message sending, history tracking, client creation |
| `tests/test_web_app.py` | FastAPI app: static file serving, chat endpoint streaming, session continuity, validation errors, error handling and rollback, logging |
| `tests/test_web_errors.py` | Friendly error pool: size, uniqueness, helper returns valid entries |
| `tests/conftest.py` | Shared fixtures: fake API key, mocked anthropic client, configured FastAPI TestClient |

## Config Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies: anthropic, httpx, python-dotenv |
| `.env` | Your `ANTHROPIC_API_KEY` (gitignored, never committed) |
| `.gitignore` | Keeps secrets and build artifacts out of git |

## How It All Connects

1. You run `python main.py`
2. `main.py` calls `personality.py` → `build_system_prompt()`
3. `personality.py` reads all files in `knowledge/` and calls `github_client.py` for fresh repo data
4. The assembled system prompt + deflection examples go to Claude with each message
5. You chat. Claude responds as Josh. Loop until you quit.
