"""Train both models, attack them, and write a results report.

Run with:  python -m src.evaluate
"""
import json
import random
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from .attacks import ATTACKS
from .data import load_data, split
from .model import baseline_model, hardened_model

RESULTS = Path(__file__).resolve().parent.parent / "results"


def clean_metrics(model, X, y):
    p = model.predict(X)
    return {
        "accuracy": round(accuracy_score(y, p), 4),
        "precision": round(precision_score(y, p), 4),
        "recall": round(recall_score(y, p), 4),
        "f1": round(f1_score(y, p), 4),
    }


def evasion_rate(model, spam_messages):
    """Share of spam the model caught before the attack that it misses afterwards."""
    caught = [m for m in spam_messages if model.predict([m])[0] == 1]
    rates = {}
    for name, attack in ATTACKS.items():
        attacked = [attack(m) for m in caught]
        missed = sum(model.predict(attacked) == 0)
        rates[name] = round(missed / len(caught), 4) if caught else 0.0
    return rates, len(caught)


def adversarial_training_set(X, y, seed=1):
    """Defence 3: add copies of training spam padded with words taken from real (ham) training
    messages, so the model learns that padding does not make spam innocent. The padding words
    come from the training data, not from the attack's word list, so the test is not rigged."""
    rng = random.Random(seed)
    ham_words = " ".join(X[y == 0]).split()
    spam = X[y == 1]
    extra = pd.Series([m + " " + " ".join(rng.choice(ham_words) for _ in range(15)) for m in spam])
    return pd.concat([X, extra], ignore_index=True), pd.concat([y, pd.Series([1] * len(extra))], ignore_index=True)


def run():
    df = load_data()
    X_train, X_test, y_train, y_test = split(df)
    spam_test = list(X_test[y_test == 1])

    models = {"baseline": baseline_model(), "hardened": hardened_model()}
    models["baseline"].fit(X_train, y_train)
    X_adv, y_adv = adversarial_training_set(X_train.reset_index(drop=True), y_train.reset_index(drop=True))
    models["hardened"].fit(X_adv, y_adv)

    results = {"dataset": {"messages": len(df), "spam": int(df.y.sum()), "test_size": len(X_test)}}
    for name, model in models.items():
        rates, n_caught = evasion_rate(model, spam_test)
        results[name] = {"clean": clean_metrics(model, X_test, y_test),
                         "spam_caught_before_attack": n_caught, "evasion_rate": rates}

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "results.json").write_text(json.dumps(results, indent=2))
    (RESULTS / "report.md").write_text(report(results))
    print(report(results))
    return results


def report(r):
    b, h = r["baseline"], r["hardened"]
    lines = [
        "## Results",
        "",
        f"Dataset: {r['dataset']['messages']} SMS messages ({r['dataset']['spam']} spam), "
        f"{r['dataset']['test_size']} held out for testing.",
        "",
        "### Clean test set",
        "",
        "| Model | Accuracy | Precision | Recall | F1 |",
        "|---|---|---|---|---|",
    ]
    for name, m in (("Baseline", b), ("Hardened", h)):
        c = m["clean"]
        lines.append(f"| {name} | {c['accuracy']:.3f} | {c['precision']:.3f} | {c['recall']:.3f} | {c['f1']:.3f} |")
    lines += [
        "",
        "### Evasion rate under attack (lower is better)",
        "",
        "Share of test spam each model caught before the attack but missed after it.",
        "",
        "| Attack | Baseline | Hardened |",
        "|---|---|---|",
    ]
    for attack in b["evasion_rate"]:
        lines.append(f"| {attack} | {b['evasion_rate'][attack]:.1%} | {h['evasion_rate'][attack]:.1%} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    run()
