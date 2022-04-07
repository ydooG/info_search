import json

from path import ROOT


TOKENS_PATH = ROOT + '/task2/static/tokens.txt'


def get_all_words(path):
    all_words = list()
    with open(path, mode='r') as file:
        for line in file:
            word = line[:-1]
            all_words.append(word)
    return all_words


def get_document_vector(path, all_words):
    tf_idfs = dict()
    vector = list()
    with open(path, mode='r') as document:
        for line in document:
            tf_idfs[line.split(':')[0]] = float(line.split(' ')[2][:-1])

    for word in all_words:
        if word in tf_idfs.keys():
            vector.append(tf_idfs[word])
        else:
            vector.append(0)

    return vector


def main():
    all_words = get_all_words(TOKENS_PATH)
    vector_space = list()
    for i in range(1, 101):
        path = ROOT + f'/task4/static/token_tf_idf/{i}.txt'
        vector_space.append(get_document_vector(path, all_words))

    for doc in vector_space:
        print(' '.join(map(str, doc)))

    with open(ROOT + '/task5/static/vector_space.json', mode='w') as file:
        file.write(json.dumps(vector_space))
    print('Количество документов:', len(vector_space))
    print('Количество уникальных слов (токенов):', len(vector_space[0]))


if __name__ == '__main__':
    main()
