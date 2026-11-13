from src.evaluate import run


def test_end_to_end_results():
    r = run()
    # The hardened model must stay accurate on normal messages...
    assert r["hardened"]["clean"]["f1"] >= 0.90
    # ...and be far harder to evade than the baseline with character tricks
    for attack in ("leetspeak", "homoglyph", "zero_width"):
        assert r["hardened"]["evasion_rate"][attack] <= 0.05
        assert r["hardened"]["evasion_rate"][attack] < r["baseline"]["evasion_rate"][attack]
