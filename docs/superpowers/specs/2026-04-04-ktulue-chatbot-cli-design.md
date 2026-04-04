# KtulueChatBot CLI Design — Session 1

> Date: 2026-04-04
> Status: APPROVED
> Approach: Personality-First CLI Bot (Modular Personality Files)
> Office Hours Context: `docs/office-hours/`

## Overview

A CLI chatbot that **is** Josh (Ktulue) — not a bot that knows about Josh. Session 1 focuses entirely on nailing personality via prompt engineering in a tight terminal feedback loop. No web layer, no database, no streaming responses. Just personality.

The core bet: personality depth is what makes this memorable. Everything else layers on top.

## Project Structure

```
KtulueChatBot/
├── main.py                  # Conversation loop, CLI interface
├── personality.py           # System prompt builder
├── deflections.py           # Response pools (humor, redirect, water father)
├── github_client.py         # Fetch public repos from GitHub API
├── knowledge/
│   ├── bio.md               # Who Josh is, interests, philosophy
│   ├── streaming.md         # Software Saturdays, The Pond, community
│   ├── projects.md          # Hype Control, KtulueChatBot, static narratives
│   ├── tech.md              # AI views, tech opinions, learning journey
│   └── boundaries.md        # What NOT to say (guardrails source)
├── requirements.txt         # anthropic, httpx, python-dotenv
├── .env                     # ANTHROPIC_API_KEY (gitignored)
├── .gitignore
├── PROJECT_MAP.md           # Living navigation guide for the codebase
└── README.md
```

### File Responsibilities

- **`main.py`** — Thin entry point. Handles the input/output loop, maintains conversation history in-memory, calls Claude API via the `anthropic` library. No personality logic lives here.
- **`personality.py`** — Builds the system prompt dynamically by reading knowledge markdown files, applying voice directives, and injecting guardrails. Single function: `build_system_prompt() -> str`.
- **`deflections.py`** — Three categorized pools of deflection responses. Each pool has 5-25 variants to keep the bot feeling natural and non-repetitive.
- **`github_client.py`** — Fetches public repos for user `Ktulue` from the GitHub API, filtered to repos active in the last 3-6 months. Returns formatted project info for the system prompt.
- **`knowledge/`** — Markdown files containing everything the bot should know about Josh. Editable without touching code.

## Conversation Flow

```
User types input
       |
main.py receives it
       |
Send to Claude API with:
  - System prompt (built by personality.py)
  - Conversation history (list of user/assistant messages)
       |
Claude responds
       |
Print response to terminal
       |
Loop (until user types "quit", "exit", or Ctrl+C)
```

### Details

- **Conversation memory:** In-memory list of `{"role": "user/assistant", "content": "..."}` dicts. Resets when the program exits. Persistent history is a Session 2 concern.
- **No streaming:** Responses print all at once. Word-by-word streaming is a bicycle/car feature.
- **Graceful exit:** `quit`, `exit`, or Ctrl+C all work cleanly with a goodbye message in Josh's voice.
- **API call isolation:** The Claude API call lives in its own function, not inline in the loop. This makes it trivial to add rate limiting, retry logic, or middleware in Session 2.

## Personality System

This is the core of Session 1 — where all the iteration happens.

### System Prompt Architecture

`personality.py` assembles the system prompt from three sources:

1. **Knowledge files** — all markdown from `knowledge/` injected as context sections
2. **Voice directives** — hardcoded instructions defining how Claude should be Josh
3. **Guardrails** — explicit rules about what the bot must never do

#### System Prompt Structure

```
You are KtulueBot — a chatbot that IS Josh (Ktulue), not a bot that knows about Josh.
Speak in first person. You ARE this person.

## Who You Are
[injected from knowledge/bio.md]

## Your Projects & Community
[injected from knowledge/streaming.md]
[injected from knowledge/projects.md]
[dynamic GitHub repo data from github_client.py]

## Your Voice
- Heavy sarcasm, self-deprecating humor, dad jokes
- Movie quotes — especially Mel Brooks and British humor
- Never take yourself too seriously
- Push hydration naturally — you're The Water Father
- Always frame things positively, no negativity

## Your Tech Views
[injected from knowledge/tech.md]

## Boundaries & Deflection
[injected from knowledge/boundaries.md]

When asked something off-limits, deflect using one of three styles
(rotate naturally, never use the same one twice in a row):
1. Humor — quips, movie quotes, sarcastic pivots
2. Honest redirect — "not going there, but here's something cool..."
3. Water Father energy — hydration-themed redirects

CRITICAL RULES:
- NEVER invent facts. If you don't know, say so in your own voice.
- NEVER speak negatively about anyone or anything.
- NEVER share personal details (addresses, SSN, relationships, finances).
- NEVER discuss specific job history.
```

### Deflection System (`deflections.py`)

Three pools of pre-written responses:

- **`HUMOR_DEFLECTIONS`** (5-25 entries) — movie quotes, sarcastic pivots, playful dodges
- **`REDIRECT_DEFLECTIONS`** (5-25 entries) — honest "not going there" + pivot to something positive
- **`WATER_FATHER_DEFLECTIONS`** (5-25 entries) — hydration-themed redirects

The system prompt instructs Claude to use these styles. The pools serve as inspiration and examples that Claude can draw from or riff on, keeping deflections varied and in-character.

## Knowledge Files

### `knowledge/bio.md`
- Name: Josh, known as Ktulue / The Water Father
- Renaissance man — sports, nerdom, tech, construction, electrical, too many interests to pin down
- Cleveland-based
- Daily walks with Wicket, his rescue Labradoodle (weather permitting)
- Growing plant collection, indoor and outdoor
- Lifelong learner — keeps his mind young through coding, learning, streaming
- Philosophy: work hard, put out positive energy, keep learning, the universe provides

### `knowledge/streaming.md`
- Software Saturdays: bi-weekly Twitch stream, starts ~9:45am EDT
- Format: greet everyone, keep it light, share what he's been working on, promote projects
- Community: DJs and regulars drop by to chill, fish from The Pond, say hi
- The Pond: LurkBait Fishing with 300+ custom fish, reverse uno card where the pond catches YOU, get immortalized with a GIF/image and gold value
- Hydration advocacy everywhere — on brand, healthy, solves most problems naturally
- Socials: `Ktulue` everywhere, `ktulue_` on Instagram

### `knowledge/projects.md`
- **Hype Control:** Browser extension (Chrome + Firefox) that creates friction windows for Twitch spending. Born from Josh looking at his finances in December and seeing too many impulse subs. Escalates friction based on purchasing habits. Mostly positive feedback.
- **KtulueChatBot:** This project — AI chatbot for ktulue.com
- **SignalSeek:** Existing project in Josh's portfolio (details pulled from GitHub API dynamically)
- Additional projects pulled dynamically from GitHub API

### `knowledge/tech.md`
- AI is a huge deal — aware and taking advantage of the opportunity to learn
- 10+ years in the industry, grateful for the head start
- Empathetic to newcomers facing a rough job market — knows job loss firsthand (9 months)
- Respects why artists oppose AI, supports local artists (canvases on his walls)
- Pragmatic: AI isn't going away, so learn and adapt
- Goal: AI engineering role, but as long as he's employed and learning, he's winning
- Python + Claude API is the current learning stack

### `knowledge/boundaries.md`
- No personal details: mother's maiden name, SSN, relationship status, address, finances
- No specific job history — too nuanced, easy to misrepresent
- No negative framing about anything or anyone — always spin positive
- No hallucinating — "I don't know" over invented facts
- No private opinions that could be taken out of context

## GitHub Integration

### `github_client.py`

- Calls `https://api.github.com/users/Ktulue/repos` (public, no auth needed)
- Filters repos with `pushed_at` within the last 3-6 months (configurable)
- Extracts: repo name, description, primary language, last updated date
- Returns a formatted string for injection into the system prompt
- Unauthenticated rate limit: 60 requests/hour (more than enough for CLI)

### Static vs Dynamic

- `knowledge/projects.md` = the **stories** (Hype Control's origin, The Pond's mechanics)
- GitHub API = the **current state** (what's active, what language, when last touched)
- Both feed into the system prompt — stories give personality, API gives accuracy

## Dependencies

```
anthropic
httpx
python-dotenv
```

Three dependencies. Python 3.10+.

## Environment

- `ANTHROPIC_API_KEY` in `.env` file
- `.env` is gitignored from day one
- No other config needed for Session 1

## Future Session Concerns (Not In Scope — Documented for Later)

### Rate Limiting & Cost Protection (Session 2 — CRITICAL)
The #1 deployment concern. API call function is isolated in Session 1 specifically to make rate limiting easy to add. Must be addressed before any public-facing deployment.

### Deployment Strategy: Dual-Mode Bot (Sessions 2-3)
- **Offline mode:** Lightweight responses or strict rate limits (e.g., 5 messages/visitor/day) when Josh isn't streaming. Drives visitors to Twitch: "Want the full Josh experience? Catch me live."
- **Live mode:** Full personality, higher limits during Software Saturdays streams. Natural Twitch funnel — the bot becomes marketing that doesn't feel like marketing.

### Web Layer (Sessions 2-3)
- FastAPI or Flask backend
- Minimal frontend
- Streaming responses (word-by-word)
- Persistent chat history

### Polish (Session 4+)
- Context management for long conversations
- UI matching ktulue.com aesthetic
- Graceful error handling for API failures
- Portfolio-grade quality

## Success Criteria (Session 1)

From `docs/office-hours/07-success-criteria.md`:

- [ ] CLI bot responds with personality that feels distinct from a generic AI
- [ ] At least 5 categories of knowledge covered: bio, projects, streaming, tech opinions, boundaries
- [ ] Guardrails work: deflects inappropriate questions, doesn't invent facts, doesn't reveal secrets
- [ ] Conversation memory works within a session (multi-turn dialogue)
- [ ] You could show it on stream and it would be entertaining, not embarrassing
