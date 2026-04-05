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
