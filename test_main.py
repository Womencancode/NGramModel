from unittest import TestCase
import Main


class TestMain(TestCase):

    #
    #
    # def test_tokenize(self):
    #     # TODO

    def test_parse_punctuation(self):
        main = Main()
        toy_corpus = 'I ,have|[] a :big h~()ouse! _The? "boat is blue.;'
        expected = 'I have a big house! The? boat is blue.'
        actual = main.parse_punctuation(toy_corpus)
        self.assertEquals(expected, actual)

