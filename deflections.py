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
