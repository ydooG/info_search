from path import ROOT
from task2.token_and_lemma import get_tokens_from_file, get_lemmas_from_file


def get_tokens():
    with open(ROOT + '/task2/static/tokens.txt', mode='r') as file:
        return set(map(lambda word: word[:-1], file.readlines()))


def get_lemmas():
    with open(ROOT + '/task2/static/lemmas.txt', mode='r') as file:
        return set(map(lambda line: line.split(':')[0], file.readlines()))


def generate_inverted_index(lemma=False):
    if lemma:
        check_set = get_lemmas()
    else:
        check_set = get_tokens()

    inverted_index = dict()
    paths = [f'{ROOT}/task1/static/pages/{i}.html' for i in range(1, 101)]
    for i, path in enumerate(paths, 1):
        if lemma:
            file_words = get_lemmas_from_file(path)
        else:
            file_words = get_tokens_from_file(path)
        for word in file_words:
            if word in check_set:
                if word in inverted_index.keys():
                    inverted_index[word].add(i)
                else:
                    inverted_index[word] = {i}
        if i % 5 == 0:
            print(f'Handled {i}/100')
    return inverted_index


def write_inverted_index_to_file(inverted_index, filename):
    with open(ROOT + f'/task3/static/{filename}', mode='w') as file:
        for token, pages in inverted_index.items():
            file.write(f'{str(token)}: {" ".join(map(str, sorted(pages)))}\n')


def main():
    inverted_index = generate_inverted_index()
    write_inverted_index_to_file(inverted_index, filename='inverted_index.txt')
    print('Generated inverted_index.txt\n')
    lemma_inverted_index = generate_inverted_index(lemma=True)
    write_inverted_index_to_file(lemma_inverted_index, filename='lemma_inverted_index.txt')
    print('Generated lemmas_inverted_index.txt')


if __name__ == '__main__':
    main()
