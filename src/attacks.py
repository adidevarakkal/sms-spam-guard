"""Evasion attacks a spammer could use to slip past a text classifier.

Each attack keeps the message readable to a human but changes the
characters or words the model sees.
"""
import random

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
# Latin letters swapped for visually identical Cyrillic letters
HOMOGLYPHS = {"a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х"}
ZERO_WIDTH = "​"
BENIGN_WORDS = "ok see you at home later thanks love mum dinner tonight lol".split()


def leetspeak(text):
    return "".join(LEET.get(ch.lower(), ch) for ch in text)


def homoglyph(text):
    return "".join(HOMOGLYPHS.get(ch, ch) for ch in text)


def zero_width(text):
    return ZERO_WIDTH.join(text)


def spacing(text):
    """'FREE prize' -> 'F R E E p r i z e'"""
    return " ".join(" ".join(word) for word in text.split())


def good_words(text, n=15, seed=0):
    """Pad the message with innocent-looking words to drown out spam signals."""
    rng = random.Random(seed)
    return text + " " + " ".join(rng.choice(BENIGN_WORDS) for _ in range(n))


ATTACKS = {
    "leetspeak": leetspeak,
    "homoglyph": homoglyph,
    "zero_width": zero_width,
    "spacing": spacing,
    "good_words": good_words,
}
