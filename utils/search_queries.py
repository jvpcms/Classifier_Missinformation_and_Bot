from config.envconfig import get_config

from functools import partial
from nltk.data import path as nltk_path
from nltk.tokenize import word_tokenize as nltk_word_tokenize
from nltk.corpus import stopwords as nltk_stopwords


config = get_config()
nltk_path.append(config.envs.nltk_data_path)
portuguese_word_tokenize = partial(nltk_word_tokenize, language=config.envs.language)
portuguese_stopwords = set(nltk_stopwords.words(config.envs.language))


def get_custom_stopwords() -> set[str]:
    """Get stopwords for portuguese language adding default stopwords and custom stopwords."""

    custom_stopwords = set(
        [
            "#Verificamos:",
            "Checamos",
            "Agência",
            "Lupa",
            "Pública",
            "Aos",
            "Fatos",
            "fatos",
            "Fake",
            "FAKE",
            "fake",
            ",",
            ":",
            ";",
            "mentira",
            "verdade",
            "falso",
            ".",
            "O",
            "A",
            "Os",
            "As",
            "Em",
            "Na",
            "No",
            "|",
            "G1",
            "g1",
        ]
    )

    return portuguese_stopwords.union(custom_stopwords)
