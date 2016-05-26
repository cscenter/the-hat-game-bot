import pickle
from sklearn.svm import SVC
from nltk.stem import SnowballStemmer

import algorithms


def is_cognates(word_1, word_2):
    with open('data/cognates_model', 'rb') as f:
        clf = pickle.load(f)

    stemmer = SnowballStemmer("russian")
    word_1 = stemmer.stem(word_1)
    word_2 = stemmer.stem(word_2)

    features = [
                algorithms.levenshtein(word_1, word_2) / max(len(word_1), len(word_2)),
                abs(len(word_1) - len(word_2)),
                len(algorithms.lcs(word_1, word_2)) / max(len(word_1), len(word_2))
               ]


    result = clf.predict([features])

    return True if result[0] == 1 else False
