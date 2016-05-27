import pandas as pd
from nltk.tokenize import WordPunctTokenizer
import pymorphy2


morph = pymorphy2.MorphAnalyzer()

text = open('data/all_mid_utf8_stemmed.txt', 'r').read()

tokens = WordPunctTokenizer().tokenize(text)

def ngrams(token_list):
    unigrams = {}
    bigrams = {}
    unigram_count = 0
    bigram_count = 0
    for i in range(len(token_list)-1):
        if '.,/:;-'.find(token_list[i]) > -1:
            continue
        unigrams[token_list[i]] = unigrams.get(token_list[i], 0) + 1
        unigram_count += 1

        if '.,/:;-'.find(token_list[i+1]) > -1:
            continue
        bigrams[token_list[i] + ' ' + token_list[i+1]] = bigrams.get(token_list[i] + ' ' + token_list[i+1], 0) + 1
        bigram_count += 1

    for key in unigrams.keys():
        unigrams[key] /= unigram_count

    for key in bigrams.keys():
        bigrams[key] /= bigram_count

    ngram1_list = [0] * len(bigrams)
    ngram2_list = [0] * len(bigrams)
    prob_list = [0] * len(bigrams)
    temp = [0] * len(bigrams)

    for i, (key, value) in enumerate(bigrams.items()):
        bg_tuple = tuple(key.split(' '))
        ngram1_list[i], ngram2_list[i], prob_list[i] = bg_tuple[0], bg_tuple[1], value

    bigrams_splitted = pd.DataFrame(
        data = list(zip(ngram1_list, ngram2_list, prob_list, temp)), columns=['fst', 'snd', 'prob', 'temp']
    )


    return unigrams, bigrams_splitted

unigrams, bigrams = ngrams(tokens)


def inflect(adjective, noun):
    try:
        p = morph.parse(noun)
        gender = p[0].tag.gender
        number = p[0].tag.number
        form = set()

        if gender is not None:
            form.add(gender)

        if number is not None:
            form.add(number)

        p_adj = morph.parse(adjective)[0]

        return p_adj.inflect(form)[0]

    except BaseException:
        return adjective


def get_description(word):
    top = bigrams[bigrams['snd'] == word + '_S'].sort_values(['prob'], ascending=False)[:20]

    for index, row in top.iterrows():
        top.loc[index, 'temp'] = row['prob'] / unigrams[row['fst']]

    result = top.sort_values(['temp'], ascending=False)['fst'].values.tolist()
    return list(map(lambda x: inflect(x[:-2], word), filter(lambda x: x[-2:] == '_A', result)))
