import math

from pymorphy2 import MorphAnalyzer

from path import ROOT
from task2.token_and_lemma import get_tokens_from_file, clean_tokens
from task3.helpers import InvertedIndex


def get_tfs_for_file(path, lemmatize=False) -> dict:
    tf = dict()
    tokens = clean_tokens(get_tokens_from_file(path))
    if lemmatize:
        morph = MorphAnalyzer()
        lemma_func = lambda token: morph.parse(str(token).lower())[0].normal_form
        tokens = list(map(lemma_func, tokens))
    for token in tokens:
        tf[token] = tokens.count(token) / len(tokens)
    return tf


def get_idfs(lemmatize=False):
    morph = MorphAnalyzer()
    if lemmatize:
        mode = 'lemma'
    else:
        mode = 'token'
    index = InvertedIndex(mode)
    idfs = dict()
    for token, docs in index.items():
        df = len(docs)
        idf = math.log(100/df)  # 100 - amount of docs
        if lemmatize:
            token = morph.parse(str(token).lower())[0].normal_form
        idfs[token] = idf
    return idfs


def write_result_to_file(path, tfs, idfs):
    with open(path, mode='w') as file:
        for token, tf in tfs.items():
            idf = idfs.get(token)
            if idf:
                tf_idf = tf * idf
                file.write(f'{token}: {idf} {tf_idf}\n')


def main():
    paths = [f'{ROOT}/task1/static/pages/{i}.html' for i in range(1, 101)]
    token_idf_s = get_idfs()
    lemma_idf_s = get_idfs(lemmatize=True)
    for i, path in enumerate(paths, 1):
        tokens_tf_s = get_tfs_for_file(path)
        token_output_path = f'{ROOT}/task4/static/token_tf_idf/{i}.txt'
        write_result_to_file(token_output_path, tokens_tf_s, token_idf_s)

        lemmas_tf_s = get_tfs_for_file(path, lemmatize=True)
        lemma_output_path = f'{ROOT}/task4/static/lemma_tf_idf/{i}.txt'
        write_result_to_file(lemma_output_path, lemmas_tf_s, lemma_idf_s)
        if i % 5 == 0:
            print(f'Handled {i}/100 files')


if __name__ == '__main__':
    main()
