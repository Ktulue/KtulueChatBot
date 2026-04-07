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

## Running the Web Server

The chatbot is also available as a streaming web app. Same personality, same knowledge base, just in a browser instead of a terminal.

Install dependencies (if you haven't already):

```
pip install -r requirements.txt
```

Start the server:

```
uvicorn web.app:app --reload
```

Open `http://localhost:8000` in your browser. The page is a dark chat interface that matches the ktulue.com aesthetic. Each browser tab is its own independent conversation. Refresh or close the tab to start a fresh session.

Server logs (including a full conversation transcript at INFO level) are written to stdout in the terminal where you ran the `uvicorn` command. Errors are logged at ERROR level with full tracebacks.

---

## Support

☕ [Buy me a coffee on Ko-fi](http://ko-fi.com/ktulue)

Created by Ktulue | The Water Father 🌊
