from gensim import models
from cognates_classifier import is_cognates
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s'
    , level=logging.INFO
)

w2v = models.Word2Vec.load_word2vec_format(
            'data/ruscorpora.model.bin.gz'
            , binary=True
            , encoding='utf-8'
        )


def normalize(word):
    return word.lower() + '_S'


def delete_tag(word):
    return word[ : len(word) - word[::-1].find('_') - 1 ]


def get_most_similar(word):
    return w2v.most_similar(word)

def get_most_mutural_by_rank(word):
    result = []
    for neighbor, _ in get_most_similar(word):
        for rank, nei_of_nei in enumerate(w2v.most_similar(neighbor)):
            if nei_of_nei[0] == word:
                result.append(neighbor)
                break
    return result


def get_description(word):
    word = normalize(word)
    result = []
    for neighbor in get_most_mutural_by_rank(word):
        if not is_cognates(delete_tag(word), delete_tag(neighbor)):
            result.append(delete_tag(neighbor))
    return result
