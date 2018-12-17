import sys
from unittest import TestCase
from Main import Main
from pympler.asizeof import asizeof


class TestMain(TestCase):

    def setUp(self):
        self.main = Main()
        self.corpus1 = 'I ,have|[] a :big h~()ouse! _The? "boat is light-blue.;'
        self.corpus2 = 'There is a potato on my foot. There is foot on my potato. The potato that is on my foot has ' \
                       'a foot on it.'
        self.corpus3 = 'I like Python programming.'
        self.corpus4 = 'I like Python programming. But I like machine learning even more, I do.'
        self.corpus2_tokens_n2 = ['#start#', 'there', 'is', 'a', 'potato', 'on', 'my', 'foot', '#end#', '#start#',
                                  'there', 'is', 'foot', 'on', 'my', 'potato', '#end#', '#start#', 'the', 'potato',
                                  'that', 'is', 'on', 'my', 'foot', 'has', 'a', 'foot', 'on', 'it', '#end#']
        self.corpus3_tokens_n2 = ['#start#', 'i', 'like', 'python', 'programming', '#end#']
        self.corpus3_tokens_n3 = ['#start#', '#start#', 'i', 'like', 'python', 'programming', '#end#']
        self.corpus3_tokens_n4 = ['#start#', '#start#', '#start#', 'i', 'like', 'python', 'programming', '#end#']

    def tearDown(self):
        self.main = None

    def test_tokenize_n2(self):
        expected = ['#start#', 'i', 'have', 'a', 'big', 'house', '#end#', '#start#', 'the', '#end#', '#start#',
                    'boat', 'is', 'light-blue', '#end#']
        actual = self.main.tokenize(corpus=self.corpus1, n=2)
        self.assertEqual(expected, actual)

    def test_tokenize_n4(self):
        expected = ['#start#', '#start#', '#start#', 'i', 'have', 'a', 'big', 'house', '#end#', '#start#', '#start#',
                    '#start#', 'the', '#end#', '#start#', '#start#', '#start#', 'boat', 'is', 'light-blue', '#end#']
        actual = self.main.tokenize(corpus=self.corpus1, n=4)
        self.assertEqual(expected, actual)

    def test__parse_punctuation(self):
        expected = 'I have a big house #end# The #end# boat is light-blue #end#'
        actual = self.main._parse_punctuation(corpus=self.corpus1)
        self.assertEqual(expected, actual)

    def test__make_ngrams_pre_word_True(self):
        expected = ('i', 'like', 'python')
        actual = self.main._make_ngrams(corpus_tokens=self.corpus3_tokens_n4, corpus_index=6, n=4,
                                        make_pre_word_ngram=True)
        self.assertEqual(expected, actual)

    def test__make_ngrams_pre_word_False(self):
        expected = ('i', 'like', 'python', 'programming')
        actual = self.main._make_ngrams(corpus_tokens=self.corpus3_tokens_n4, corpus_index=6, n=4,
                                        make_pre_word_ngram=False)
        self.assertEqual(expected, actual)

    def test_make_ngrams_and_pre_word_ngrams(self):
        expected = {('#start#', '#start#', '#start#', 'i'): ('#start#', '#start#', '#start#'),
                    ('#start#', '#start#', 'i', 'like'): ('#start#', '#start#', 'i'),
                    ('#start#', 'i', 'like', 'python'): ('#start#', 'i', 'like'),
                    ('i', 'like', 'python', 'programming'): ('i', 'like', 'python')}
        actual = self.main.make_ngrams_and_pre_word_ngrams(corpus_tokens=self.corpus3_tokens_n4, n=4)
        self.assertEqual(expected, actual)

    def test_compute_probabilities_per_word(self):
        """
        'There is a potato on my foot. There is foot on my potato. The potato that is on my foot has a foot on it.'
        (sum(there|#start#) = 2 / sum(#start#) = 3) = 2/3
        (sum(is|there) = 2 / sum(there) = 2) = 1
        (sum(a|is) = 1 / sum(is) = 3) = 1/3
        (sum(potato|a) = 1 / sum(a) = 2) = 1/2
        (sum(on|potato) = 1 / sum(potato) = 3) = 1/3
        (sum(my|on) = 3 / sum(on) = 4) = 3/4
        (sum(foot|my) = 2 / sum(my) = 3) = 2/3
        (sum(foot|is) = 1 / sum(is) = 3) = 1/3
        (sum(on|foot) = 2 / sum(foot) = 4) = 2/4
        (sum(potato|my) = 1 / sum(potato) = 3) = 1/3
        (sum(the|#start#) = 1 / sum(#start#) = 3) = 1/3
        (sum(potato|the) = 1 / sum(the) = 1) = 1
        (sum(that|potato) = 1 / sum(potato) = 3) = 1/3
        (sum(is|that) = 1 / sum(that) = 1) = 1
        (sum(on|is) = 1 / sum(is) = 3) = 1/3
        (sum(has|foot) = 1 / sum(foot) = 4) = 1/4
        (sum(a|has) = 1 / sum(has) = 1) = 1
        (sum(foot|a) = 1 / sum(a) = 2) = 1/2
        (sum(it|on) = 1 / sum(on) = 4) = 1/4
        2/3 x 1 x 1/3 x 1/2 x 1/3 x 3/4 x 2/3 x 1/3 x 2/4 x 1/3 x 1/3 x 1 x 1/3 x 1 x 1/3 x 1/4 x 1 x 1/2 x 1/4
        """
        expected = {('#start#', 'there'): 2 / 3, ('there', 'is'): 1 / 1, ('is', 'a'): 1 / 3, ('a', 'potato'): 1 / 2,
                    ('potato', 'on'): 1 / 3, ('on', 'my'): 3 / 4, ('my', 'foot'): 2 / 3, ('is', 'foot'): 1 / 3,
                    ('foot', 'on'): 2 / 4, ('my', 'potato'): 1 / 3, ('#start#', 'the'): 1 / 3, ('the', 'potato'): 1 / 1,
                    ('potato', 'that'): 1 / 3, ('that', 'is'): 1 / 1, ('is', 'on'): 1 / 3, ('foot', 'has'): 1 / 4,
                    ('has', 'a'): 1 / 1, ('a', 'foot'): 1 / 2, ('on', 'it'): 1 / 4}
        actual = self.main.compute_probabilities_per_word(corpus=self.corpus2, n=2)
        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test__count_occurrences(self):
        expected = {('#start#', 'i'): 1, ('i', 'like'): 1, ('like', 'python'): 1, ('python', 'programming'): 1}
        actual = self.main._count_occurrences(corpus_tokens=self.corpus3_tokens_n2, window_size=2)
        self.assertEqual(expected, actual)

    # def test_measure_sze_of_objects(self):
    #     print('Size of main object: ' + str(sys.getsizeof(self.main, set())))
    #     print('Deep size of main object: ' + str(asizeof(self.main, set())))

    def test_compute_likelihood(self):
        """
        corpus4: 'I like Python programming. But I like machine learning even more, I do.'
        test_corpus = 'I like'
        (sum(i|#start#) = 1 / sum(#start#) = 2) = 1/2
        (sum(like|i) = 2 / sum(i) = 3) = 2/3
        product = 1/2 x 2/3 = 1/3
        """
        expected = 1 / 3
        actual = self.main.compute_likelihood(corpus=self.corpus4, test_corpus='I like', n=2)
        self.assertEqual(expected, actual)

    def test_compute_perplexity(self):
        expected = 1.2457309396155174
        actual = self.main.compute_perplexity(corpus=self.corpus4, test_corpus='I like', n=2)
        self.assertIsInstance(actual, float)
        self.assertEqual(expected, actual)
