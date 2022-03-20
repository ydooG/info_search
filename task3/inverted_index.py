from path import ROOT
from task2.token_and_lemma import get_tokens_from_file


def get_tokens():
    with open(ROOT + '/task2/static/tokens.txt', mode='r') as file:
        return set(map(lambda word: word[:-1], file.readlines()))


def generate_inverted_index():
    tokens = get_tokens()
    inverted_index = dict()
    paths = [f'{ROOT}/task1/static/pages/{i}.html' for i in range(1, 101)]
    for i, path in enumerate(paths, 1):
        raw_tokens = get_tokens_from_file(path)
        for token in tokens:
            if token in raw_tokens:
                if token in inverted_index.keys():
                    inverted_index[token].append(i)
                else:
                    inverted_index[token] = [i]
        if i % 5 == 0:
            print(f'Handled {i}/100')
    return inverted_index


def write_inverted_index_to_file(inverted_index):
    with open(ROOT + '/task3/static/inverted_index.txt', mode='w') as file:
        for token, pages in inverted_index.items():
            file.write(f'{str(token)}: {" ".join(map(str, pages))}\n')


def main():
    inverted_index = generate_inverted_index()
    write_inverted_index_to_file(inverted_index)


if __name__ == '__main__':
    main()
