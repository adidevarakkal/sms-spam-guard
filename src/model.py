"""Two models: an undefended baseline and a hardened version."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .defence import normalise


def baseline_model():
    """Word-level TF-IDF + logistic regression, no defences."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])


def hardened_model():
    """Normalise the text, then use character n-grams, which survive small spelling tricks."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=normalise, analyzer="char_wb",
                                  ngram_range=(3, 5), min_df=2, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", C=10)),
    ])
