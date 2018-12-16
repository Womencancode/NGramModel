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
        :return: Tokenized corpus, as a list of words representing the input corpus, preserving word order.
        """
        corpus = self._parse_punctuation(corpus)
        corpus = corpus.lower()
        corpus_tokens = corpus.split()
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

    def make_ngrams_and_pre_word_ngrams(self, corpus_tokens: list, n: int):
        """
        Make lists of n-grams paired to the preceding (n-1)-gram with the whole n-gram as the key and the preceding
        words as the value. For example: where n=4, the 4-gram list for word D is [A,B,C,D]. The key-value paired
        lists are: [A,B,C,D]:[A,B,C].
        :param corpus_tokens: Tokenized corpus, as produced by self.tokenize(corpus).
        :param n: Size of the n-gram (as number of words).
        :return: Lists of n-gram paired to their preceding (n-1)-gram.
        """
        ngrams_and_pre_words: dict = {}
        first_word_i = n - 1
        end_i = len(corpus_tokens) - 1
        for i in range(first_word_i, end_i):
            pre_words_ngrams = self._make_pre_words_ngram(corpus_tokens, i, n)
            current_token = (corpus_tokens[i],)
            ngrams = tuple(pre_words_ngrams) + current_token
            if self.Strs.END.value in ngrams:
                continue
            else:
                ngrams_and_pre_words[ngrams] = pre_words_ngrams
        return ngrams_and_pre_words

    def _make_pre_words_ngram(self, corpus_tokens: list, corpus_index: int, n: int):
        """
        Make list of words that precede current word (at corpus_index) according to size n-gram.
        :param corpus_tokens: Tokenized corpus, as produced by self.tokenize(corpus).
        :param corpus_index: Position of current word token according to 0-indexing.
        :param n: Size of n-gram (as number of words).
        :return: List of words that precede current word in corpus.
        """
        pre_words_ngram = []
        if corpus_index - (n - 1) >= 0:
            for i in range(n - 1, 0, -1):
                pre_words_ngram.append(corpus_tokens[corpus_index - i])
        return tuple(pre_words_ngram)

    def compute_probabilities_per_word(self, corpus: str, n: int):
        """
        Compute a list of probabilities of n-grams in a corpus, sampled with a sliding window of one word,
        in natural order of English text (from left to right).
        :param corpus: Space-delimited words.
        :param n: Size of the n-gram (as number of words).
        :return: List of n-grams each paired with their computed probability.
        """
        corpus_tokens = self.tokenize(corpus, n)
        ngrams_and_pre_word_ngrams = self.make_ngrams_and_pre_word_ngrams(corpus_tokens, n)
        ngram_occurrences = self._count_occurrences(corpus_tokens, n)
        pre_ngram_occurrences = self._count_occurrences(corpus_tokens, n - 1)
        probs_per_ngram = {}
        for ngram, pre_ngram in ngrams_and_pre_word_ngrams.items():
            probs_per_ngram[ngram] = ngram_occurrences[ngram] / pre_ngram_occurrences[pre_ngram]
        return probs_per_ngram

    def _count_occurrences(self, corpus_tokens: list, num: int):
        ngram_occurrences = {}
        for i, corpus_token in enumerate(corpus_tokens):
            ngram = []
            if i + num > len(corpus_tokens) - 1:
                break
            else:
                for j in range(num):
                    ngram.append(corpus_tokens[i + j])
                if self.Strs.END.value in ngram:
                    continue
                else:
                    ngram_key = tuple(ngram)
                    if ngram_key in ngram_occurrences:
                        ngram_occurrences[ngram_key] += 1
                    else:
                        ngram_occurrences[ngram_key] = 1
        return ngram_occurrences

    # def count_occurrences(self, corpus_tokens: str):
    #     """
    #     Count the number of occurrences of each word (token).
    #     :param corpus_tokens: Tokenized corpus, as produced by self.tokenize(corpus).
    #     :return: Number of occurrences of a token as key-value pairs, with tokens as the key and number of
    #     occurrences as the associated value)
    #     """
    #     token_counts = Counter(corpus_tokens)
    #     return token_counts

    from enum import Enum

    class Strs(Enum):
        STRT = '#start#'
        END = '#end#'
