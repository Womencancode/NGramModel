import re
from collections import Counter


class Main(object):

    def tokenize(self, corpus: str, n: int):
        """
        Convert a corpus to a list of lowercase words using white space as the delimiter, preserving the order of
        words. Insert #start#(s) at start of sentences according to the size of the n-gram, replace punctuation that
        terminates a sentence with #end#. Remove all other punctuation.
        :param corpus: Space-delimited words.
        :param n: Size of the n-gram (as number of words).
        :return: List of tokens representing the input corpus, preserving word order.
        """
        corpus = self._parse_punctuation(corpus)
        corpus = corpus.lower()
        corpus_tokens = corpus.split(' ')
        for i in range(n - 1):
            corpus_tokens.insert(0, self.Strs.STRT.value)
        if corpus_tokens[len(corpus_tokens) - 1] != self.Strs.END.value:
            corpus_tokens.append(self.Strs.END.value)
        end_indices = [i for i, x in enumerate(corpus_tokens) if x == self.Strs.END.value and i != len(corpus_tokens)
                       - 1]
        inserted_starts = 0
        for i, end_index in enumerate(end_indices):
            insert_start_index = end_index + 1
            for j in range(n - 1):
                corpus_tokens.insert(insert_start_index + inserted_starts, self.Strs.STRT.value)
                inserted_starts += 1
        return corpus_tokens

    def _parse_punctuation(self, corpus: str):
        """
        Removes any punctuation. Replaces punctuation that terminates a sentence with #end#.
        :param corpus: Space-delimited words.
        :return: Corpus with punctuation removed or replaced with #end#.
        """
        pattern_nonstop_punct = re.compile(r'[][{},;:()/~"_|]+')
        pattern_stop_punct = re.compile('[.!?]+')
        corpus = pattern_nonstop_punct.sub('', corpus)
        corpus = pattern_stop_punct.sub(' ' + self.Strs.END.value, corpus)
        return corpus

    def make_pre_word_ngrams(self, corpus_tokens: list, n: int):
        """
        Make a list of n-gram words that precede each word, sampling the corpus with a sliding window of one word.
        E.g. corpus_tokens=['#start#', 'i', 'like', 'python', 'programming', '#end#'] and n=3 would produce:
        [['#start#','#start#'],['#start#','i'], ['i','like'],['like','python']]
        :param corpus_tokens: A corpus stored as a list of words produced by self.tokenize(corpus_tokens).
        :param n: Size of the n-gram (as number of words).
        :return:
        """
        first_word_i = n - 1
        end_i = len(corpus_tokens) - 1
        pre_words_ngrams = [self._get_preceeding_words(corpus_tokens, i, n) for i in range(first_word_i, end_i)]
        return pre_words_ngrams

    def _get_preceeding_words(self, corpus_tokens: list, corpus_index: int, n: int):
        pre_words = []
        if corpus_index - (n - 1) >= 0:
            for i in range(n - 1, 0, -1):
                pre_words.append(corpus_tokens[corpus_index - i])
        return pre_words

    def count_occurrences(self, corpus_tokens: str):
        """
        Count the number of occurrences of each word (token).
        :param corpus_tokens: A corpus stored as a list of words produced by self.tokenize(corpus_tokens).
        :return: Number of occurrences of a token as key-value pairs, with tokens as the key and number of
        occurrences as the associated value)
        """
        token_counts = Counter(corpus_tokens)
        return token_counts

    from enum import Enum

    class Strs(Enum):
        STRT = '#start#'
        END = '#end#'
