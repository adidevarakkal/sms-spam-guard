"""Defences: undo character tricks before the model sees the text."""
import re
import unicodedata

from .attacks import HOMOGLYPHS, LEET

REVERSE_HOMOGLYPHS = {v: k for k, v in HOMOGLYPHS.items()}
REVERSE_LEET = {v: k for k, v in LEET.items()}
INVISIBLE = re.compile("[​‌‍⁠﻿]")
SPACED_LETTERS = re.compile(r"\b(?:\w ){2,}\w\b")


def _de_leet_word(word):
    # Only translate digits inside words that also contain letters ("fr33" -> "free"),
    # so real numbers such as phone numbers and prices are left alone.
    if any(c.isalpha() for c in word) and any(c in REVERSE_LEET for c in word):
        return "".join(REVERSE_LEET.get(c, c) for c in word)
    return word


def normalise(text):
    text = unicodedata.normalize("NFKC", text)
    text = INVISIBLE.sub("", text)
    text = "".join(REVERSE_HOMOGLYPHS.get(ch, ch) for ch in text)
    text = SPACED_LETTERS.sub(lambda m: m.group(0).replace(" ", ""), text)
    text = " ".join(_de_leet_word(w) for w in text.split())
    return text.lower()
