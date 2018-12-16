from unittest import TestCase
from Main import Main
import sys
from pympler.asizeof import asizeof


class TestMain(TestCase):

    def setUp(self):
        self.main = Main()
        self.toy_corpus = 'I ,have|[] a :big h~()ouse! _The? "boat is light-blue.;'
        self.toy_corpus_2 = 'There is a potato on my foot. There is foot on my potato. The potato that is on my foot ' \
                            'has a foot on it.'
        self.corpus_tokens_2 = ['#start#', 'there', 'is', 'a', 'potato', 'on', 'my', 'foot', '#end#', '#start#',
                                'there', 'is', 'foot', 'on', 'my', 'potato', '#end#', '#start#', 'the', 'potato',
                                'that', 'is', 'on', 'my', 'foot', 'has', 'a', 'foot', 'on', 'it', '#end#']
        self.corpus_tokens_3 = ['#start#', 'i', 'like', 'python', 'programming', '#end#']

    def tearDown(self):
        self.main = None
        self.toy_corpus = None

    def test_tokenize(self):
        expected = ['#start#', 'i', 'have', 'a', 'big', 'house', '#end#', '#start#', 'the', '#end#', '#start#',
                    'boat', 'is', 'light-blue', '#end#']
        actual = self.main.tokenize(self.toy_corpus)
        self.assertEqual(expected, actual)

    def test_parse_punctuation(self):
        expected = 'I have a big house #end# The #end# boat is light-blue #end#'
        actual = self.main.parse_punctuation(self.toy_corpus)
        self.assertEqual(expected, actual)

    def test_count_occurences(self):
        expected = {'#start#': 3, 'there': 2, 'is': 3, 'a': 2, 'potato': 3, 'on': 4, 'my': 3, 'foot': 4, '#end#': 3,
                    'the': 1, 'that': 1, 'has': 1, 'it': 1}
        actual = self.main.count_occurences(self.corpus_tokens_2)
        self.assertEqual(expected, actual)
        print(str(asizeof(self.main, set())))

    def test__add_extra_start_tokens(self):
        expected = ['#start#', '#start#', '#start#', 'i', 'like', 'python', 'programming', '#end#']
        actual = self.main._add_extra_start_tokens(self.corpus_tokens_3, 4)
        self.assertEqual(expected, actual)

    # def test_measure_sze_of_objects(self):
    #     print('Size of main object: ' + str(sys.getsizeof(self.main, set())))
    #     print('Deep size of main object: ' + str(asizeof(self.main, set())))

    # def test_make_ngrams_indexed(self):

    def test_get_preceeding_words(self):
        expected = ['there', 'is', 'a']
        actual = self.main.get_preceeding_words(self.corpus_tokens_2, 4, 4)
        self.assertEqual(expected, actual)

    def test_make_pre_word_ngrams(self):
        expected = [['#start#', '#start#', '#start#'], ['#start#', '#start#', 'i'], ['#start#', 'i', 'like'],
                    ['i', 'like', 'python']]
        actual = self.main.make_pre_word_ngrams(self.corpus_tokens_3, 4)
        self.assertEqual(expected, actual)
