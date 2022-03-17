import nltk
from bs4 import BeautifulSoup
from pymorphy2 import MorphAnalyzer


def get_text_from_file(path):
    with open(path, mode='r') as file:
        soup = BeautifulSoup(file.read(), features='html.parser')
        texts = ' '.join(soup.find('article').stripped_strings)
        return nltk.word_tokenize(texts, language='russian')


def clean_tokens(tokens):
    cleaned_tokens = set()
    morph = MorphAnalyzer()
    for token in tokens:
        l_token = str(token).lower()
        if l_token:
            morphed_token = morph.parse(l_token)[0]
            # проверка на предлог и союз
            if morphed_token.tag.POS and morphed_token.tag.POS not in ['CONJ', 'PREP']\
                    and all([tag not in morphed_token.tag for tag in ['LATN', 'NUMB']]):  # проверка на число и латиницу
                cleaned_tokens.add(token)
    return cleaned_tokens


def write_tokens_to_file(tokens):
    with open('static/tokens.txt', mode='w') as file:
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
    with open('static/lemmas.txt', mode='w') as file:
        for lemma, tokens in lemmas.items():
            file.write(f'{lemma}: {" ".join(tokens)}\n')


def main():
    paths = [f'../task1/static/pages/{i}.html' for i in range(1, 101)]
    raw_tokens = list()
    for path in paths:
        raw_tokens.extend(get_text_from_file(path))
    tokens = clean_tokens(raw_tokens)
    write_tokens_to_file(tokens)
    lemmas = get_lemmas(tokens)
    write_lemmas_to_file(lemmas)


if __name__ == '__main__':
    main()
