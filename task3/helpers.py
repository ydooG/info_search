from path import ROOT


class InvertedIndex(dict):
    def __init__(self):
        super().__init__()
        self._initialize()

    def _initialize(self):
        with open(ROOT + '/task3/static/inverted_index.txt', mode='r') as file:
            for line in file:
                items = line[:-1].split(': ')
                self[items[0]] = set(map(int, items[1].split(' ')))

    def __getitem__(self, item):
        if item in self.keys():
            return dict.__getitem__(self, item)
        else:
            return set()
