from unittest import TestCase
from Main import Main
import sys
from pympler.asizeof import asizeof


class TestMain(TestCase):

    def setUp(self):
        self.main = Main()
        self.corpus1 = 'I ,have|[] a :big h~()ouse! _The? "boat is light-blue.;'
        self.corpus2 = 'There is a potato on my foot. There is foot on my potato. The potato that is on my foot  has ' \
                       'a foot on it.'
        self.corpus3 = 'I like Python programming.'
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

    def test_make_pre_word_ngrams_n3(self):
        expected = [['#start#', '#start#'], ['#start#', 'i'], ['i', 'like'], ['like', 'python']]
        actual = self.main.make_pre_word_ngrams(corpus_tokens=self.corpus3_tokens_n3, n=3)
        self.assertEqual(expected, actual)

    def test_make_pre_word_ngrams_n4(self):
        expected = [['#start#', '#start#', '#start#'], ['#start#', '#start#', 'i'], ['#start#', 'i', 'like'],
                    ['i', 'like', 'python']]
        actual = self.main.make_pre_word_ngrams(corpus_tokens=self.corpus3_tokens_n4, n=4)
        self.assertEqual(expected, actual)

    def test__get_preceeding_words(self):
        expected = ['i', 'like', 'python']
        actual = self.main._get_preceeding_words(corpus_tokens=self.corpus3_tokens_n4, corpus_index=6, n=4)
        self.assertEqual(expected, actual)

    def test_count_occurences(self):
        expected = {'#start#': 3, 'there': 2, 'is': 3, 'a': 2, 'potato': 3, 'on': 4, 'my': 3, 'foot': 4, '#end#': 3,
                    'the': 1, 'that': 1, 'has': 1, 'it': 1}
        actual = self.main.count_occurrences(corpus_tokens=self.corpus2_tokens_n2)
        self.assertEqual(expected, actual)
        print(str(asizeof(self.main, set())))

    # def test_measure_sze_of_objects(self):
    #     print('Size of main object: ' + str(sys.getsizeof(self.main, set())))
    #     print('Deep size of main object: ' + str(asizeof(self.main, set())))
