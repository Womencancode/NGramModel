import re
from collections import Counter


class Main(object):

    # def __init__(self):
    #     pass

    def tokenize(self, corpus_tokens: str):
        corpus_tokens = self.parse_punctuation(corpus_tokens)
        corpus_tokens = corpus_tokens.lower()
        corpus_tokens = corpus_tokens.split(' ')
        corpus_tokens.insert(0, self.Strs.STRT.value)
        if corpus_tokens[len(corpus_tokens) - 1] != self.Strs.END.value:
            corpus_tokens.append(self.Strs.END.value)
        end_indices = [i for i, x in enumerate(corpus_tokens) if x == self.Strs.END.value and i != len(corpus_tokens)
                       - 1]
        for i, end_index in enumerate(end_indices):
            corpus_tokens.insert(end_index + i + 1, self.Strs.STRT.value)
        return corpus_tokens

    def parse_punctuation(self, corpus: str):
        pattern_nonstop_punct = re.compile(r'[][{},;:()/~"_|]+')
        pattern_stop_punct = re.compile('[.!?]+')
        corpus = pattern_nonstop_punct.sub('', corpus)
        corpus = pattern_stop_punct.sub(self.Strs.END.value, corpus)
        return corpus

    def count_occurences(self, corpus_tokens: str):
        token_counts = Counter(corpus_tokens)
        return token_counts

    def make_pre_word_ngrams(self, corpus_tokens: list, n: int):
        corpus_tokens = self._add_extra_start_tokens(corpus_tokens, n)
        pre_words_ngrams = [self.get_preceeding_words(corpus_tokens, i, n) for i in range(len(corpus_tokens))]
        return pre_words_ngrams

    def get_preceeding_words(self, corpus_tokens: list, corpus_index: int, n: int):
        pre_words = []
        if corpus_index - (n - 1) < 0:
            for i in range(n - 1):
                pre_words.append(self.Strs.STRT.value)
        else:
            for i in range(n - 1, 0, -1):
                pre_words.append(corpus_tokens[corpus_index - i])
        return pre_words

    def _add_extra_start_tokens(self, corpus_tokens: list, n: int):
        if n < 2:
            print('A bi-gram only requires 1 start token at beginning of corpus. No extra starts to be added.')
        else:
            num_of_extra_start_tokens_to_add = n - 2
            for i in range(num_of_extra_start_tokens_to_add):
                corpus_tokens.insert(0, self.Strs.STRT.value)
        return corpus_tokens

    from enum import Enum

    class Strs(Enum):
        STRT = '#start#'
        END = '#end#'
