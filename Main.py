import re


class Main(object):

    def __init__(self):
        print(' nothing')

    def tokenize(self, corpus: str):
        corpus = self.parse_punctuation(corpus)
        corpus = corpus.lower()
        corpus = corpus.split(' ')
        corpus.insert(0, '#start#')
        if corpus[len(corpus) - 1] != '#end#':
            corpus.append('#end#')
        end_indices = [i for i, x in enumerate(corpus) if x == '#end#' and i != len(corpus) - 1]
        for i, end_index in enumerate(end_indices):
            corpus.insert(end_index + i + 1, '#start#')

    def parse_punctuation(self, corpus: str):
        pattern_nonstop_punct = re.compile(r'[][{},;:()/~"|]+')
        pattern_stop_punct = re.compile('[.!?]+')
        corpus = pattern_nonstop_punct.sub('', corpus)
        corpus = pattern_stop_punct.sub(' #end#', corpus)
        return corpus
