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
