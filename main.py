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
    stream: bool = True,
) -> str:
    """Send a message to Claude and return the response text.

    Appends both the user message and assistant response to history.
    When stream=True, prints tokens as they arrive.
    """
    history.append({"role": "user", "content": user_input})

    if stream:
        collected = []
        print()
        print("KtulueBot: ", end="", flush=True)
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=history,
        ) as response:
            for text in response.text_stream:
                print(text, end="", flush=True)
                collected.append(text)
        print()
        assistant_text = "".join(collected)
    else:
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

            send_message(client, system_prompt, history, user_input)
            print()

    except KeyboardInterrupt:
        print()
        print()
        print("KtulueBot: Ctrl+C? Respect. Don't forget your water! Later! 🌊")


if __name__ == "__main__":
    main()
