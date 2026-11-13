# Learning notes

## Why this project

My 43030 learning plan had two goals I had not finished:

- **Goal 2, cybersecurity:** the module's applied assessment asks for an analysis of a threat, its impact and a defence strategy. "Adversarial attacks on machine learning schemes" is one of its listed topics.
- **Goal 4, machine learning extension:** build end-to-end model projects, using the freeCodeCamp *Machine Learning with Python* curriculum as a guide.

This project does both: it builds an ML model, attacks it, and defends it.

## Method borrowed from freeCodeCamp

freeCodeCamp teaches ML by building small, complete projects that are checked by automated tests. One of its certification projects is an SMS text classifier. I used the same approach here, without copying its solution:

| freeCodeCamp approach | How I applied it |
|---|---|
| Learn by building one complete project | Data loading, model, evaluation and report, all in one repo |
| Automated tests decide whether it works | `pytest` tests run on every push in GitHub Actions |
| Clear success criteria | Tests require F1 >= 0.90 and evasion <= 5% for character attacks |

I still plan to complete the freeCodeCamp certification itself separately (see my report's future goals). This project is not a submission for it.

## What I learned

- A model can score 98% accuracy and still be trivially evaded: the clean test set says nothing about an attacker.
- Defences belong in the pipeline (preprocessing and features), not just in the model.
- An evaluation can accidentally be rigged. My first adversarial-training version padded spam with the same word list the attack used, which made the defence look better than it was. Switching to words from the real training messages gave an honest, higher residual evasion rate.
- Security results should report what still gets through, not just what was blocked.
