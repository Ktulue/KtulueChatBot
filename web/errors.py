"""In-character error messages shown to visitors when something goes wrong server-side."""
import random


FRIENDLY_ERRORS = [
    "My brain just buffered. Hydrate while I reboot.",
    "Connection's choppier than my Wi-Fi during a stream. Try that one again?",
    "Something tripped a wire backstage. Give me a sec and try that again.",
    "Looks like I knocked my water bottle onto the keyboard. One moment.",
    "The Water Father's pipes are clogged. One more try should do it.",
    "Brain fog. Real brain fog. Hit me with that question one more time?",
]


def pick_friendly_error() -> str:
    """Return a random friendly error message from the pool."""
    return random.choice(FRIENDLY_ERRORS)
