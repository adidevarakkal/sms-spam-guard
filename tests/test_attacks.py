from src.attacks import ATTACKS, ZERO_WIDTH, spacing, zero_width

MSG = "FREE prize call now"


def test_every_attack_changes_the_message():
    for name, attack in ATTACKS.items():
        assert attack(MSG) != MSG, name


def test_spacing_splits_letters():
    assert spacing("win now") == "w i n n o w"


def test_zero_width_is_invisible_but_present():
    attacked = zero_width("win")
    assert attacked.replace(ZERO_WIDTH, "") == "win"
    assert attacked.count(ZERO_WIDTH) == 2
