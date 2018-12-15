from unittest import TestCase
from Main import Main


class TestMain(TestCase):

    def setUp(self):
        self.main = Main()
        self.toy_corpus = 'I ,have|[] a :big h~()ouse! _The? "boat is light-blue.;'

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

