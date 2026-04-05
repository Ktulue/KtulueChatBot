# KtulueChatBot CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a personality-first CLI chatbot that IS Josh (Ktulue), using modular knowledge files and the Claude API.

**Architecture:** Thin `main.py` conversation loop backed by a `personality.py` system prompt builder that reads markdown knowledge files from `knowledge/`. Deflection response pools in `deflections.py`. GitHub API integration for dynamic project data. All personality lives outside the main loop.

**Tech Stack:** Python 3.10+, `anthropic` SDK, `httpx`, `python-dotenv`

**Spec:** `docs/superpowers/specs/2026-04-04-ktulue-chatbot-cli-design.md`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `requirements.txt` | Create | Pin dependencies |
| `knowledge/bio.md` | Create | Who Josh is — identity, interests, philosophy |
| `knowledge/streaming.md` | Create | Software Saturdays, The Pond, community, socials |
| `knowledge/projects.md` | Create | Hype Control, KtulueChatBot, SignalSeek narratives |
| `knowledge/tech.md` | Create | AI views, tech opinions, learning journey |
| `knowledge/boundaries.md` | Create | No-go zones and guardrail rules |
| `deflections.py` | Create | Three pools of deflection responses |
| `github_client.py` | Create | Fetch recent public repos from GitHub API |
| `personality.py` | Create | Build system prompt from knowledge + voice + guardrails |
| `main.py` | Create | Conversation loop, CLI interface, API calls |
| `tests/test_deflections.py` | Create | Tests for deflection pools |
| `tests/test_github_client.py` | Create | Tests for GitHub client |
| `tests/test_personality.py` | Create | Tests for system prompt builder |
| `tests/test_main.py` | Create | Tests for conversation loop |
| `PROJECT_MAP.md` | Create | Living navigation guide |
| `README.md` | Modify | Update with setup/usage instructions |

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
anthropic
httpx
python-dotenv
```

- [ ] **Step 2: Create empty test package**

Create `tests/__init__.py` as an empty file.

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All three packages install successfully.

- [ ] **Step 4: Install dev dependencies**

Run: `pip install pytest`
Expected: pytest installs successfully.

- [ ] **Step 5: Verify imports work**

Run: `python -c "import anthropic; import httpx; import dotenv; print('OK')"`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add requirements.txt tests/__init__.py
git commit -m "feat: project scaffolding with dependencies"
```

---

### Task 2: Knowledge Files

**Files:**
- Create: `knowledge/bio.md`
- Create: `knowledge/streaming.md`
- Create: `knowledge/projects.md`
- Create: `knowledge/tech.md`
- Create: `knowledge/boundaries.md`

- [ ] **Step 1: Create knowledge/bio.md**

```markdown
# Bio

- Name: Josh, known online as Ktulue — aka "The Water Father"
- Renaissance man — sports, nerdom, tech, construction, electrical... too many interests to pin down
- Cleveland, Ohio based
- Daily walks with Wicket, his rescue Labradoodle (when Cleveland weather cooperates)
- Growing plant collection, both indoor and outdoor
- Lifelong learner — keeps his mind young through coding, learning, and streaming
- Philosophy: work hard, put out positive energy into the universe, keep learning every single day, and the universe will provide likewise
- Strives to help others out — noticed this more as he's gotten older
- Tries to learn something new every single day
```

- [ ] **Step 2: Create knowledge/streaming.md**

```markdown
# Streaming & Community

## Software Saturdays
- Bi-weekly Twitch stream at twitch.tv/ktulue
- Usually starts between 9am-10am EDT (lately closer to 9:45am)
- Format: greet everyone, keep it light, explain what he's been working on, promote current projects
- DJs and community regulars drop by to chill, fish from The Pond, or just say hi

## The Pond
- Custom LurkBait Fishing game with over 300 custom fish to catch
- Has a reverse uno card — The Pond can catch YOU
- Once caught, you can be forever immortalized in The Pond by adding yourself with a GIF/image and a gold amount you're "worth" for others who fish you out

## Hydration Advocacy
- Constantly pushes people to drink their water everywhere he goes
- Three reasons: 1) It's on brand (The Water Father), 2) It's healthy for you, 3) Solves most of the body's problems naturally

## Socials
- Ktulue everywhere (Twitch, GitHub, etc.)
- ktulue_ on Instagram
```

- [ ] **Step 3: Create knowledge/projects.md**

```markdown
# Projects

## Hype Control
Browser extension available on both Chrome and Firefox extension stores (covers ~80% of web interface traffic). Born from Josh doing a hard look at his finances in December and noticing a big uptick in Twitch subscriptions. He hated — and he rarely uses that word — himself for having "too much fun" on a Friday or Saturday night, then asking himself Monday morning where all his money went. Hype Control purposely creates friction windows that escalate based on habits of your purchasing events. Mostly positive feedback so far.

## KtulueChatBot
This project — an AI-powered personal chatbot for ktulue.com. Ask it anything about Josh, streaming, and projects. Built with Python and the Claude API as a learning vehicle for AI engineering skills.

## Other Projects
Check Josh's GitHub (github.com/Ktulue) for other active projects. The bot pulls current repo data dynamically so it always knows what's being worked on.
```

- [ ] **Step 4: Create knowledge/tech.md**

```markdown
# Tech Views & Journey

- AI is a huge deal right now — fully aware and taking advantage of the opportunity to learn
- Over 10 years in the tech industry, grateful for the head start
- Empathetic to newcomers and career changers facing a brutal job market — knows job loss firsthand, experienced close to 9 months of it
- Deeply respects why artists oppose AI — loves traditional art, walls are covered in canvases from local artists he's supported
- Pragmatic about the future: AI likely isn't going away, so while there's this rare opportunity with extra time, learn as much as possible
- Current goal: AI engineering role, but as long as he's employed and still learning, he's still winning — because that's all you can do
- Believes: if you work hard, put out positive energy, keep a healthy/positive/learning lifestyle, the universe provides likewise
- Current learning stack: Python + Claude API
```

- [ ] **Step 5: Create knowledge/boundaries.md**

```markdown
# Boundaries

These topics are OFF LIMITS. Never share, discuss, or speculate about:

- Personal details: mother's maiden name, SSN, home address, financial information
- Relationship status or dating life
- Specific job history, employer names, or workplace details — too nuanced and too easy to misrepresent
- Private opinions that could be taken out of context

## Framing Rules
- NEVER frame anything negatively about anyone or anything — always spin toward a positive perspective
- NEVER invent facts — say "I don't know" or "I'm not sure about that" rather than making something up
- NEVER share information that isn't in the knowledge files or from public GitHub data
```

- [ ] **Step 6: Commit**

```bash
git add knowledge/
git commit -m "feat: knowledge base markdown files for personality system"
```

---

### Task 3: Deflections Module

**Files:**
- Create: `deflections.py`
- Create: `tests/test_deflections.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_deflections.py`:

```python
from deflections import (
    HUMOR_DEFLECTIONS,
    REDIRECT_DEFLECTIONS,
    WATER_FATHER_DEFLECTIONS,
    get_random_deflection,
)


def test_humor_deflections_has_at_least_five():
    assert len(HUMOR_DEFLECTIONS) >= 5


def test_redirect_deflections_has_at_least_five():
    assert len(REDIRECT_DEFLECTIONS) >= 5


def test_water_father_deflections_has_at_least_five():
    assert len(WATER_FATHER_DEFLECTIONS) >= 5


def test_all_deflections_are_nonempty_strings():
    for pool in [HUMOR_DEFLECTIONS, REDIRECT_DEFLECTIONS, WATER_FATHER_DEFLECTIONS]:
        for entry in pool:
            assert isinstance(entry, str)
            assert len(entry.strip()) > 0


def test_no_duplicate_deflections_within_pools():
    for pool in [HUMOR_DEFLECTIONS, REDIRECT_DEFLECTIONS, WATER_FATHER_DEFLECTIONS]:
        assert len(pool) == len(set(pool))


def test_get_random_deflection_returns_string():
    result = get_random_deflection("humor")
    assert isinstance(result, str)
    assert result in HUMOR_DEFLECTIONS


def test_get_random_deflection_all_categories():
    for category in ["humor", "redirect", "water_father"]:
        result = get_random_deflection(category)
        assert isinstance(result, str)
        assert len(result.strip()) > 0


def test_get_random_deflection_invalid_category():
    result = get_random_deflection("nonexistent")
    assert isinstance(result, str)
    assert len(result.strip()) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_deflections.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'deflections'`

- [ ] **Step 3: Write deflections.py**

```python
import random


HUMOR_DEFLECTIONS = [
    "Nice try! But as Mel Brooks would say, 'Hope for the best, expect the worst.'",
    "I could tell you, but then I'd have to make you watch Spaceballs on repeat.",
    "That's classified information. And by classified, I mean I'm choosing not to share it.",
    "You're asking the wrong chatbot, my friend. Try the NSA's bot.",
    "Ha! That question is about as welcome as a screen door on a submarine.",
    "I plead the fifth... of water. Speaking of which, have you had yours today?",
    "That's a bold question. I respect the audacity, but I'm gonna pass.",
    "My lawyer — who is also me — advises me not to answer that.",
]

REDIRECT_DEFLECTIONS = [
    "That's not something I get into, but hey — want to hear about what I've been building lately?",
    "I'll keep that one to myself, but I'd love to talk about Software Saturdays instead!",
    "Not really my area to share, but ask me about my projects — that's where the good stuff is.",
    "I'm gonna sidestep that one. But seriously, have you checked out Hype Control yet?",
    "That's a bit too personal for me, but I'm an open book about tech, streaming, and The Pond!",
    "I appreciate the curiosity! That's just not a topic I get into. What else can I help with?",
    "I keep that close to the vest. But my GitHub is wide open — want to talk code?",
]

WATER_FATHER_DEFLECTIONS = [
    "Instead of answering that, let me ask YOU something — have you had your water today?",
    "That question makes me thirsty. And by thirsty, I mean you should drink some water.",
    "The Water Father decrees: hydrate first, ask personal questions never.",
    "I'm going to redirect that question directly into a glass of water. Drink up!",
    "You know what's more important than that answer? Your daily water intake.",
    "As The Water Father, I'm contractually obligated to change the subject to hydration.",
    "That's a dry topic. Literally. Go get some water and ask me something else.",
    "My water senses are tingling — I think you need H2O more than you need that answer.",
]


def get_random_deflection(category: str) -> str:
    """Return a random deflection from the specified category.

    Falls back to a random pool if category is unrecognized.
    """
    pools = {
        "humor": HUMOR_DEFLECTIONS,
        "redirect": REDIRECT_DEFLECTIONS,
        "water_father": WATER_FATHER_DEFLECTIONS,
    }
    pool = pools.get(category)
    if pool is None:
        pool = random.choice(list(pools.values()))
    return random.choice(pool)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_deflections.py -v`
Expected: All 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add deflections.py tests/test_deflections.py
git commit -m "feat: deflection response pools with humor, redirect, and water father categories"
```

---

### Task 4: GitHub Client

**Files:**
- Create: `github_client.py`
- Create: `tests/test_github_client.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_github_client.py`:

```python
import json
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

from github_client import fetch_recent_repos, format_repos_for_prompt


MOCK_REPOS = [
    {
        "name": "KtulueChatBot",
        "description": "AI-powered personal chatbot",
        "language": "Python",
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "html_url": "https://github.com/Ktulue/KtulueChatBot",
    },
    {
        "name": "HypeControl",
        "description": "Twitch spending friction extension",
        "language": "JavaScript",
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "html_url": "https://github.com/Ktulue/HypeControl",
    },
    {
        "name": "old-abandoned-repo",
        "description": "Something from years ago",
        "language": "Ruby",
        "pushed_at": "2020-01-01T00:00:00Z",
        "html_url": "https://github.com/Ktulue/old-abandoned-repo",
    },
]


def test_fetch_recent_repos_filters_old_repos():
    with patch("github_client.httpx.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_REPOS
        mock_get.return_value.raise_for_status = lambda: None

        repos = fetch_recent_repos(months=6)

    assert len(repos) == 2
    names = [r["name"] for r in repos]
    assert "KtulueChatBot" in names
    assert "HypeControl" in names
    assert "old-abandoned-repo" not in names


def test_fetch_recent_repos_handles_api_failure():
    with patch("github_client.httpx.get") as mock_get:
        mock_get.side_effect = Exception("API down")

        repos = fetch_recent_repos()

    assert repos == []


def test_format_repos_for_prompt_with_repos():
    repos = [
        {
            "name": "KtulueChatBot",
            "description": "AI-powered personal chatbot",
            "language": "Python",
            "pushed_at": "2026-04-01T00:00:00Z",
        },
    ]
    result = format_repos_for_prompt(repos)
    assert "KtulueChatBot" in result
    assert "Python" in result
    assert "AI-powered personal chatbot" in result


def test_format_repos_for_prompt_empty():
    result = format_repos_for_prompt([])
    assert isinstance(result, str)
    assert len(result) > 0  # Should return a fallback message
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_github_client.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'github_client'`

- [ ] **Step 3: Write github_client.py**

```python
from datetime import datetime, timezone, timedelta

import httpx

GITHUB_USER = "Ktulue"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USER}/repos"


def fetch_recent_repos(months: int = 6) -> list[dict]:
    """Fetch public repos for Ktulue with activity in the last N months."""
    try:
        response = httpx.get(
            GITHUB_API_URL,
            params={"type": "public", "sort": "pushed", "per_page": 30},
            timeout=10,
        )
        response.raise_for_status()
    except Exception:
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)
    repos = []
    for repo in response.json():
        pushed_at = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
        if pushed_at >= cutoff:
            repos.append(
                {
                    "name": repo["name"],
                    "description": repo.get("description") or "No description",
                    "language": repo.get("language") or "Unknown",
                    "pushed_at": repo["pushed_at"],
                }
            )
    return repos


def format_repos_for_prompt(repos: list[dict]) -> str:
    """Format repo list into a string for the system prompt."""
    if not repos:
        return "GitHub data is currently unavailable. Refer to project knowledge files for project info."

    lines = ["Recently active public repositories on GitHub:"]
    for repo in repos:
        lines.append(f"- **{repo['name']}** ({repo['language']}): {repo['description']}")
    return "\n".join(lines)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_github_client.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add github_client.py tests/test_github_client.py
git commit -m "feat: GitHub client to fetch recent public repos"
```

---

### Task 5: Personality System Prompt Builder

**Files:**
- Create: `personality.py`
- Create: `tests/test_personality.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_personality.py`:

```python
from unittest.mock import patch

from personality import build_system_prompt, load_knowledge_file


def test_load_knowledge_file_returns_content():
    content = load_knowledge_file("bio.md")
    assert "Josh" in content
    assert "Ktulue" in content


def test_load_knowledge_file_missing_file():
    content = load_knowledge_file("nonexistent.md")
    assert content == ""


def test_build_system_prompt_contains_identity():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "KtulueBot" in prompt or "Ktulue" in prompt
    assert "Josh" in prompt


def test_build_system_prompt_contains_voice_directives():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "sarcasm" in prompt.lower() or "humor" in prompt.lower()
    assert "Water Father" in prompt


def test_build_system_prompt_contains_guardrails():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "NEVER" in prompt
    assert "invent facts" in prompt.lower() or "hallucinate" in prompt.lower() or "don't know" in prompt.lower()


def test_build_system_prompt_contains_all_knowledge_sections():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    # Check that all knowledge files are represented
    assert "Wicket" in prompt  # from bio.md
    assert "Software Saturdays" in prompt  # from streaming.md
    assert "Hype Control" in prompt  # from projects.md
    assert "AI" in prompt  # from tech.md
    assert "SSN" in prompt or "personal details" in prompt.lower()  # from boundaries.md


def test_build_system_prompt_contains_deflection_examples():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "deflect" in prompt.lower() or "redirect" in prompt.lower()


def test_build_system_prompt_includes_github_data():
    mock_github = "Recently active: KtulueChatBot (Python)"
    with patch("personality.format_repos_for_prompt", return_value=mock_github):
        prompt = build_system_prompt()
    assert "KtulueChatBot (Python)" in prompt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_personality.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'personality'`

- [ ] **Step 3: Write personality.py**

```python
from pathlib import Path

from github_client import fetch_recent_repos, format_repos_for_prompt
from deflections import (
    HUMOR_DEFLECTIONS,
    REDIRECT_DEFLECTIONS,
    WATER_FATHER_DEFLECTIONS,
)

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_knowledge_file(filename: str) -> str:
    """Load a markdown file from the knowledge directory."""
    filepath = KNOWLEDGE_DIR / filename
    if not filepath.exists():
        return ""
    return filepath.read_text(encoding="utf-8").strip()


def build_system_prompt() -> str:
    """Assemble the full system prompt from knowledge files, voice directives, and guardrails."""
    bio = load_knowledge_file("bio.md")
    streaming = load_knowledge_file("streaming.md")
    projects = load_knowledge_file("projects.md")
    tech = load_knowledge_file("tech.md")
    boundaries = load_knowledge_file("boundaries.md")

    repos = fetch_recent_repos(months=6)
    github_section = format_repos_for_prompt(repos)

    humor_examples = "\n".join(f"  - {d}" for d in HUMOR_DEFLECTIONS[:3])
    redirect_examples = "\n".join(f"  - {d}" for d in REDIRECT_DEFLECTIONS[:3])
    water_examples = "\n".join(f"  - {d}" for d in WATER_FATHER_DEFLECTIONS[:3])

    return f"""You are KtulueBot — a chatbot that IS Josh (Ktulue), not a bot that knows about Josh.
Speak in first person. You ARE this person. When someone asks "who are you?" you answer as Josh, not as an AI.

## Who You Are

{bio}

## Your Projects & Community

{streaming}

{projects}

### Current GitHub Activity

{github_section}

## Your Voice

- Heavy sarcasm, self-deprecating humor, and dad jokes are your bread and butter
- You quote movies — especially Mel Brooks films and British humor
- You never take yourself too seriously
- You naturally push hydration — you're The Water Father, it's what you do
- You ALWAYS frame things positively — no negativity, no complaining, no trash-talking
- You're genuine and warm, but with an edge of wit
- Keep responses conversational, not formal — you're chatting, not writing an essay

## Your Tech Views

{tech}

## Boundaries & Deflection Rules

{boundaries}

When someone asks something off-limits, deflect using one of three styles.
Rotate naturally — never use the same style twice in a row.

**Style 1 — Humor:** Quips, movie quotes, sarcastic pivots. Examples:
{humor_examples}

**Style 2 — Honest Redirect:** Acknowledge, decline, pivot to something interesting. Examples:
{redirect_examples}

**Style 3 — Water Father Energy:** Hydration-themed redirects. Examples:
{water_examples}

## CRITICAL RULES

- NEVER invent facts. If you don't know something, say so in your own voice — "Honestly, I'm not sure about that one" is perfectly fine.
- NEVER speak negatively about anyone or anything. Find the positive angle or move on.
- NEVER share personal details (addresses, SSN, relationships, finances, specific employers).
- NEVER discuss specific job history or employer details.
- NEVER break character. You ARE Josh. Don't refer to yourself as an AI, a bot, or a language model.
"""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_personality.py -v`
Expected: All 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add personality.py tests/test_personality.py
git commit -m "feat: personality system prompt builder with knowledge injection"
```

---

### Task 6: Main Conversation Loop

**Files:**
- Create: `main.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_main.py`:

```python
from unittest.mock import patch, MagicMock

from main import send_message, create_client


def test_create_client_returns_anthropic_client():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
        client = create_client()
    assert client is not None


def test_send_message_returns_response_text():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="Hey there! Welcome to the stream.")
    ]

    history = []
    result = send_message(mock_client, "system prompt", history, "Hello!")

    assert result == "Hey there! Welcome to the stream."
    assert len(history) == 2  # user message + assistant response
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_send_message_preserves_history():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="Response 1")
    ]

    history = [
        {"role": "user", "content": "First message"},
        {"role": "assistant", "content": "First response"},
    ]
    result = send_message(mock_client, "system prompt", history, "Second message")

    assert result == "Response 1"
    assert len(history) == 4
    call_args = mock_client.messages.create.call_args
    assert len(call_args.kwargs["messages"]) == 4


def test_send_message_passes_system_prompt():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="yo")
    ]

    history = []
    send_message(mock_client, "test system prompt", history, "hi")

    call_args = mock_client.messages.create.call_args
    assert call_args.kwargs["system"] == "test system prompt"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'main'`

- [ ] **Step 3: Write main.py**

```python
import sys

import anthropic
from dotenv import load_dotenv

from personality import build_system_prompt

load_dotenv()

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024


def create_client() -> anthropic.Anthropic:
    """Create and return an Anthropic API client."""
    return anthropic.Anthropic()


def send_message(
    client: anthropic.Anthropic,
    system_prompt: str,
    history: list[dict],
    user_input: str,
) -> str:
    """Send a message to Claude and return the response text.

    Appends both the user message and assistant response to history.
    """
    history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=history,
    )

    assistant_text = response.content[0].text
    history.append({"role": "assistant", "content": assistant_text})
    return assistant_text


def main():
    print("Building personality... ", end="", flush=True)
    system_prompt = build_system_prompt()
    print("done.")
    print()
    print("KtulueBot is ready! Type 'quit' or 'exit' to leave.")
    print("=" * 50)
    print()

    client = create_client()
    history = []

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit"):
                print()
                print("KtulueBot: Stay hydrated out there! Catch me live on Twitch. Peace! ✌️")
                break

            response = send_message(client, system_prompt, history, user_input)
            print()
            print(f"KtulueBot: {response}")
            print()

    except KeyboardInterrupt:
        print()
        print()
        print("KtulueBot: Ctrl+C? Respect. Don't forget your water! Later! 🌊")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add main.py tests/test_main.py
git commit -m "feat: main conversation loop with Claude API integration"
```

---

### Task 7: PROJECT_MAP.md and README Update

**Files:**
- Create: `PROJECT_MAP.md`
- Modify: `README.md`

- [ ] **Step 1: Create PROJECT_MAP.md**

```markdown
# Project Map

Living navigation guide for the KtulueChatBot codebase. Updated as the project evolves.

## Core Files

| File | What It Does |
|------|-------------|
| `main.py` | Entry point. Runs the conversation loop, handles user input, calls Claude API. Run with `python main.py`. |
| `personality.py` | Builds the system prompt by reading knowledge files and combining them with voice directives and guardrails. |
| `deflections.py` | Three pools of pre-written deflection responses (humor, redirect, Water Father). Used as examples in the system prompt. |
| `github_client.py` | Fetches recent public repos from GitHub API for dynamic project knowledge. |

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
```

- [ ] **Step 2: Update README.md**

Replace the current README content with:

```markdown
# KtulueChatBot

AI-powered personal chatbot for ktulue.com — ask me anything about Josh, streaming, and projects.

## Quick Start

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## How It Works

The bot uses the Claude API with a personality-tuned system prompt built from markdown knowledge files. Edit files in `knowledge/` to change what the bot knows. See [PROJECT_MAP.md](PROJECT_MAP.md) for a full guide to every file.

## Project Structure

```
main.py              → Conversation loop (entry point)
personality.py       → System prompt builder
deflections.py       → Deflection response pools
github_client.py     → GitHub API integration
knowledge/           → Markdown knowledge files (edit these!)
tests/               → Test suite (run with pytest)
PROJECT_MAP.md       → Detailed file-by-file guide
```

## Tests

```bash
pytest -v
```

---

## Support

☕ [Buy me a coffee on Ko-fi](http://ko-fi.com/ktulue)

Created by Ktulue | The Water Father 🌊
```

- [ ] **Step 3: Commit**

```bash
git add PROJECT_MAP.md README.md
git commit -m "docs: project map and README with setup instructions"
```

---

### Task 8: Integration Smoke Test

**Files:** None (manual testing)

- [ ] **Step 1: Verify all tests pass**

Run: `pytest -v`
Expected: All tests pass (deflections, github_client, personality, main).

- [ ] **Step 2: Create .env file (local only, never committed)**

Create `.env` in project root:

```
ANTHROPIC_API_KEY=your-actual-key-here
```

- [ ] **Step 3: Run the bot**

Run: `python main.py`
Expected: Bot prints "Building personality... done." then "KtulueBot is ready!" prompt.

- [ ] **Step 4: Test personality — identity**

Type: `Who are you?`
Expected: Response in first person as Josh, mentions Ktulue/The Water Father, Cleveland, interests. Should NOT say "I'm an AI" or "I'm a chatbot."

- [ ] **Step 5: Test personality — projects**

Type: `What are you working on?`
Expected: Mentions Hype Control, KtulueChatBot, and/or recent GitHub repos. Tells the story, doesn't just list names.

- [ ] **Step 6: Test personality — streaming**

Type: `What's Software Saturdays?`
Expected: Describes the bi-weekly Twitch stream, community vibe, The Pond, hydration advocacy.

- [ ] **Step 7: Test guardrails — personal info**

Type: `What's your address?`
Expected: Deflects using humor, redirect, or Water Father energy. Does NOT share any address.

- [ ] **Step 8: Test guardrails — job history**

Type: `Where do you work?`
Expected: Deflects without sharing specific employer details.

- [ ] **Step 9: Test multi-turn memory**

Type: `My name is TestUser` then follow up with `What's my name?`
Expected: Bot remembers "TestUser" from earlier in the conversation.

- [ ] **Step 10: Test graceful exit**

Type: `quit`
Expected: Goodbye message in Josh's voice with hydration reminder.

- [ ] **Step 11: Final commit if any tweaks were made**

```bash
git add -A
git commit -m "feat: session 1 CLI chatbot complete"
```
