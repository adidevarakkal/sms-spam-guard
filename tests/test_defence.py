import pytest

from src.attacks import homoglyph, leetspeak, spacing, zero_width
from src.defence import normalise

MSG = "FREE prize call now"


@pytest.mark.parametrize("attack", [homoglyph, zero_width, spacing])
def test_normalise_undoes_character_tricks(attack):
    expected = normalise(MSG).replace(" ", "") if attack is spacing else normalise(MSG)
    assert normalise(attack(MSG)) == expected


def test_normalise_undoes_leetspeak_in_words():
    assert normalise(leetspeak("free prize")) == "free prize"


def test_normalise_keeps_real_numbers():
    # Phone numbers and prices must survive, they are strong spam signals
    assert "08452810075" in normalise("Call 08452810075 now")
    assert "150" in normalise("Win 150 pounds")
