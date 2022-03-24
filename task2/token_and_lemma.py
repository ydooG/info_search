import nltk
from bs4 import BeautifulSoup
from pymorphy2 import MorphAnalyzer

from path import ROOT


def get_tokens_from_file(path):
    with open(path, mode='r') as file:
        soup = BeautifulSoup(file.read(), features='html.parser')
        texts = ' '.join(soup.find('article').stripped_strings)
        return nltk.word_tokenize(texts, language='russian')


def get_lemmas_from_file(path):
    morph = MorphAnalyzer()
    with open(path, mode='r') as file:
        soup = BeautifulSoup(file.read(), features='html.parser')
        texts = ' '.join(soup.find('article').stripped_strings)
        return list(map(lambda token: morph.parse(str(token).lower())[0].normal_form,
                        nltk.word_tokenize(texts, language='russian')))


def clean_tokens(tokens) -> list:
    clean_func = lambda t: str(t).replace('…', '').replace('...', '')
    tokens = list(map(clean_func, tokens))
    cleaned_tokens = list()
    morph = MorphAnalyzer()
    for token in tokens:
        l_token = str(token).lower()
        if l_token:
            morphed_token = morph.parse(l_token)[0]
            # проверка на предлог и союз
            if morphed_token.tag.POS and morphed_token.tag.POS not in ['CONJ', 'PREP']\
                    and all([tag not in morphed_token.tag for tag in ['LATN', 'NUMB']]):  # проверка на число и латиницу
                cleaned_tokens.append(token)
    return cleaned_tokens


def write_tokens_to_file(tokens):
    with open(ROOT + '/task2/static/tokens.txt', mode='w') as file:
        for token in tokens:
            file.write(f'{token}\n')


def get_lemmas(tokens):
    morph = MorphAnalyzer()
    lemmas = dict()
    for token in tokens:
        l_token = token.lower()
        lemma = morph.parse(l_token)[0].normal_form
        if lemma not in lemmas.keys():
            lemmas[lemma] = [token]
        else:
            lemmas[lemma].append(token)
    return lemmas


def write_lemmas_to_file(lemmas):
    with open(ROOT + '/task2/static/lemmas.txt', mode='w') as file:
        for lemma, tokens in lemmas.items():
            file.write(f'{lemma}: {" ".join(tokens)}\n')


def main():
    paths = [f'{ROOT}/task1/static/pages/{i}.html' for i in range(1, 101)]
    raw_tokens = list()
    for i, path in enumerate(paths, 1):
        page_tokens = get_tokens_from_file(path)
        raw_tokens.extend(page_tokens)
        if i % 5 == 0:
            print(f'Got tokens from {i}/100 files.')
    print('Cleaning tokens...')
    tokens = set(clean_tokens(raw_tokens))
    print('Writing cleaned tokens to file')
    write_tokens_to_file(tokens)
    print('Generating lemmas file...')
    lemmas = get_lemmas(tokens)
    write_lemmas_to_file(lemmas)


if __name__ == '__main__':
    main()
