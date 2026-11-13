# SMS Spam Guard: attacking and defending a spam classifier

![Test and evaluate](https://github.com/adidevarakkal/sms-spam-guard/actions/workflows/ci.yml/badge.svg)

A small machine-learning security project. I train an SMS spam classifier, attack it the way real spammers do, measure how often the attacks get through, and then harden the model and measure again. Everything is tested and runs in GitHub Actions and Docker on every push.

Built for 43030 Professional Practice in Computing (UTS) as a combined project for my learning-plan **Goal 2 (cybersecurity)** and **Goal 4 (machine learning)**. See [LEARNING.md](LEARNING.md) for how it maps to those goals.

## The threat

Spam filters are machine-learning models, and spammers adapt to them. They do not need access to the model: they only need to change their messages so the model no longer recognises them while a human still can. This is an **evasion attack**, one of the main adversarial threats to ML systems in production.

| Attack | Example | Why it works on a naive model |
|---|---|---|
| leetspeak | `FR33 PR1Z3` | "fr33" is not a word the model learned |
| homoglyph | `FREE рrize` (Cyrillic р) | looks identical, but is a different character |
| zero_width | `F​R​E​E` (invisible characters between letters) | the word is split into pieces the model has never seen |
| spacing | `F R E E p r i z e` | every word becomes single letters |
| good_words | spam + "ok see you at home later..." | innocent words outweigh the spam signals |

## The defence

The hardened model layers three defences:

1. **Normalisation** (`src/defence.py`): Unicode NFKC, removing invisible characters, mapping look-alike letters back to Latin, rejoining spaced-out letters, and undoing leetspeak inside words (while keeping real numbers such as phone numbers).
2. **Character n-grams**: the model looks at 3 to 5 character fragments instead of whole words, so a small spelling change only affects a few features.
3. **Adversarial training**: training spam is duplicated with padding taken from real non-spam training messages, so padding stops looking like a sign of innocence. The padding comes from the training data, not the attack's word list, so the test is not rigged.

## Results

Dataset: 5572 SMS messages (747 spam), 1115 held out for testing.

### Clean test set

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Baseline | 0.983 | 0.945 | 0.926 | 0.936 |
| Hardened | 0.989 | 0.979 | 0.940 | 0.959 |

### Evasion rate under attack (lower is better)

Share of test spam each model caught before the attack but missed after it.

| Attack | Baseline | Hardened |
|---|---|---|
| leetspeak | 63.0% | 0.0% |
| homoglyph | 36.2% | 0.0% |
| zero_width | 100.0% | 0.0% |
| spacing | 100.0% | 15.7% |
| good_words | 31.2% | 10.0% |
## What the results show

- Character tricks completely beat the baseline: invisible characters and letter spacing let **every** spam message through.
- Normalisation plus character n-grams stop leetspeak, homoglyphs and zero-width tricks entirely, without hurting accuracy on normal messages (precision rose, recall dropped slightly).
- **Residual risk:** letter spacing and good-word padding still get some spam through the hardened model. Spaced text loses its word boundaries when rejoined, and padding dilutes the signal in short messages. No single defence is complete, which is why real filters combine models with sender reputation, rate limiting and link scanning.

## Run it

```bash
pip install -r requirements.txt
python -m pytest -v        # unit tests
python -m src.evaluate     # train, attack, defend; writes results/report.md
```

Or with Docker:

```bash
docker build -t sms-spam-guard .
docker run --rm sms-spam-guard
```

## Project structure

```
src/data.py       load the dataset and split it
src/attacks.py    five evasion attacks
src/defence.py    text normalisation
src/model.py      baseline and hardened models
src/evaluate.py   train, attack and report
tests/            pytest unit and end-to-end tests
.github/workflows/ci.yml   tests + evaluation + Docker on every push
```

## Data

SMS Spam Collection v.1 (Almeida & Gómez Hidalgo, UCI Machine Learning Repository, CC BY 4.0). See [data/README.md](data/README.md).

## Acknowledgement

Built with help from Claude (Anthropic) for structure and code, as declared in my 43030 report.
