import re


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
        tokenized_corpus = corpus.split()
        for i in range(n - 1):
            tokenized_corpus.insert(0, self.TOKENS.STRT.value)
        if tokenized_corpus[len(tokenized_corpus) - 1] != self.TOKENS.END.value:
            tokenized_corpus.append(self.TOKENS.END.value)
        end_indices = [i for i, x in enumerate(tokenized_corpus) if x == self.TOKENS.END.value and i != len(
            tokenized_corpus)
                       - 1]
        inserted_starts = 0
        for i, end_index in enumerate(end_indices):
            insert_start_index = end_index + 1
            for j in range(n - 1):
                tokenized_corpus.insert(insert_start_index + inserted_starts, self.TOKENS.STRT.value)
                inserted_starts += 1
        return tokenized_corpus

    def _parse_punctuation(self, corpus: str):
        """
        Removes any punctuation. Replaces punctuation that terminates a sentence with #end#.
        :param corpus: Space-delimited words.
        :return: Corpus with punctuation removed or replaced with #end#.
        """
        pattern_nonstop_punct = re.compile(r'[][{},;:()/~"_|]+')
        pattern_stop_punct = re.compile('[.!?]+')
        corpus = pattern_nonstop_punct.sub('', corpus)
        corpus = pattern_stop_punct.sub(' ' + self.TOKENS.END.value, corpus)
        return corpus

    def make_ngrams_and_pre_word_ngrams(self, tokenized_corpus: list, n: int):
        """
        Make lists of n-grams paired to the preceding (n-1)-gram, using the whole n-gram as the key and the preceding
        words (n-1)-gram as the value. For example: where n=4, the 4-gram list for word D is [A,B,C,D]. The key-value
        paired lists are: [A,B,C,D]:[A,B,C].
        :param tokenized_corpus: Tokenized corpus, as produced by self.tokenize(corpus).
        :param n: Size of the n-gram (as number of words).
        :return: Lists of n-gram paired to their preceding (n-1)-gram.
        """
        ngrams_and_pre_words = {}
        first_word_i = n - 1
        end_i = len(tokenized_corpus) - 1
        for i in range(first_word_i, end_i):
            if i - (n - 1) < 0:
                continue
            pre_words_ngrams = self._make_ngrams(tokenized_corpus, i, n, make_pre_word_ngram=True)
            current_token = (tokenized_corpus[i],)
            ngrams = pre_words_ngrams + current_token
            if self.TOKENS.END.value in ngrams:
                continue
            else:
                ngrams_and_pre_words[ngrams] = tuple(pre_words_ngrams)
        return ngrams_and_pre_words

    def _make_ngrams(self, tokenized_corpus: list, corpus_token_index: int, n: int, make_pre_word_ngram=False):
        """
        Make list of words that make up an n-gram according to size of n. Can also make the n-gram preceding each word.
        :param tokenized_corpus: Tokenized corpus, as produced by self.tokenize(corpus).
        :param corpus_token_index: Position of current word token, using zero-indexing.
        :param n: Size of n-gram (as number of words).
        :param make_pre_word_ngram: True to make n-gram of preceding words only (not including the last word token).
        :return: List of words that precede current word in corpus.
        """
        ngrams = []
        end_i = 0 if make_pre_word_ngram else -1
        for i in range(n - 1, end_i, -1):
            ngrams.append(tokenized_corpus[corpus_token_index - i])
        return tuple(ngrams)

    # NOT SURE THIS IS COMPLETE. NEEDS TESTING.
    def compute_probabilities_per_word(self, corpus: str, n: int, use_Lap_smooth=False):
        """
        Compute a list of probabilities of n-grams in a corpus, sampled with a sliding window of one word,
        in the normal left-to-right direction of English text. Can employ Laplacian smoothing by assigning occurrence
        of n-gram ending with #UNK# to 1 (sum of 0 + 1).
        :param corpus: Space-delimited words.
        :param n: Size of the n-gram (as number of words).
        :param use_Lap_smooth: True to use Laplacian smoothing.
        :return: List of n-grams each paired with their computed probability.
        """
        tokenized_corpus = self.tokenize(corpus, n)
        ngrams_and_pre_word_ngrams = self.make_ngrams_and_pre_word_ngrams(tokenized_corpus, n)
        ngram_occurrences = self._count_occurrences(tokenized_corpus, n)
        pre_ngram_occurrences = self._count_occurrences(tokenized_corpus, n - 1)
        probs_per_ngram = {}
        V = 0
        Lap_smooth_suppl = 0
        if use_Lap_smooth:
            V = self.calculate_vocabulary_size(corpus)
            Lap_smooth_suppl = 1
        for ngram, pre_ngram in ngrams_and_pre_word_ngrams.items():
            probs_per_ngram[ngram] = (ngram_occurrences[ngram] + Lap_smooth_suppl) / (pre_ngram_occurrences[
                                                                                          pre_ngram] + V)
        return probs_per_ngram

    def _count_occurrences(self, corpus_tokens: list, window_size: int):
        """
        Count number of occurrences of every n-gram in corpus list with sliding window of one word, according to 
        specified window size.
        :param corpus_tokens: Tokenized corpus, as produced by self.tokenize(corpus).
        :param window_size: Number of word tokens, typically the size of the n-gram, n or n-1 of 'pre_words'.
        :return: n-gram paired to the number of its occurrences.
        """
        ngram_occurrences = {}
        for i, corpus_token in enumerate(corpus_tokens):
            ngram = []
            if i + window_size > len(corpus_tokens) - 1:
                break
            else:
                for j in range(window_size):
                    ngram.append(corpus_tokens[i + j])
                if self.TOKENS.END.value in ngram:
                    continue
                else:
                    ngram_key = tuple(ngram)
                    if ngram_key in ngram_occurrences:
                        ngram_occurrences[ngram_key] += 1
                    else:
                        ngram_occurrences[ngram_key] = 1
        return ngram_occurrences

    # If the task required the option for Laplacian smoothing to calculate likelihood (as well as probability),
    # I would add another use_Lap_smooth boolean argument to this method as well. True would result in passing the
    # tokenized test_corpus to a method which together with the training corpus, replaces any words in the
    # test_corpus that are not found in the training corpus, with the #UNK# token. This would allow the likelihood to
    # be calculated from the probs_per_ngram data structure that would hold probabilities per n-gram ending with
    # #UNK#. But this was not a stated requirement of Task 4, so I have not done it.
    def compute_likelihood(self, corpus: str, test_corpus: str, n: int):
        """
        Calculate likelihood of a test corpus, based on the probabilities of all n-grams in a training corpus (which
        is based on the Markov assumption). The likelihood is a product of the aforementioned probabilities.
        :param corpus: Space-delimited words, used as a training corpus.
        :param test_corpus: The likelihood of all of these words in the exact order they are in, is calculated here.
        :param n: Size of the n-gram (as number of words).
        :return: Likelihood of the test corpus.
        """
        probs_per_ngram = self.compute_probabilities_per_word(corpus, n)
        test_corpus_tokens = self.tokenize(test_corpus, n)
        test_corpus_ngrams = ()
        end_i = len(test_corpus_tokens) - 1
        for i in range(end_i):
            if i - (n - 1) < 0:
                continue
            test_corpus_ngrams = test_corpus_ngrams + (self._make_ngrams(test_corpus_tokens, i, n), )
        likelihood_of_test_corpus = 1
        for test_corpus_ngram in test_corpus_ngrams:
            likelihood_of_test_corpus = likelihood_of_test_corpus * probs_per_ngram[test_corpus_ngram]
        return likelihood_of_test_corpus

    def compute_perplexity(self, train_corpus: str, test_corpus: str, n: int):
        """
        Calculate the perplexity of a test corpus, based on the likelihood of the test corpus, according to the
        equation that perplexity is the likelihood taken to the power of -1 / (length of the test corpus).
        :param train_corpus: Space-delimited words, used as a training corpus.
        :param test_corpus: The perplexity of all of these words in the exact order they are in, is calculated here.
        :param n: Size of the n-gram (as number of words).
        :return: Perplexity of the test corpus.
        """
        N = len(''.join(test_corpus.split()))
        y = -1 / N
        likelihood = self.compute_likelihood(train_corpus, test_corpus, n)
        return likelihood ** y

    def calculate_vocabulary_size(self, corpus: str):
        """
        Calculate vocabulary size of corpus (for training), as the number of distinct tokens (not including #start#
        and #end# tokens, divided by the total number of words in the corpus.
        :param corpus: Space-delimited words, used as a training corpus.
        :return: V, size of vocabulary of the corpus.
        """
        corpus_tokens_less = self._tokenize_less_start_end(corpus)
        Lap_smooth_suppl = 1
        V = (len(set(corpus_tokens_less)) + Lap_smooth_suppl) / (len(corpus_tokens_less) + Lap_smooth_suppl)
        return V

    def _tokenize_less_start_end(self, corpus: str):
        """
        Tokenize a corpus, remove #start# and #end#.
        :return: Tokenized corpus, lacking #start# and #end# tokens.
        """
        corpus_tokens = self.tokenize(corpus, 0)
        return [x for x in corpus_tokens if x != self.TOKENS.END.value]

    from enum import Enum

    class TOKENS(Enum):
        STRT = '#start#'
        END = '#end#'
