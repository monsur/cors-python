from list_validator import ListValidator
import unittest


class TestListValidator(unittest.TestCase):

    def test_emptyList(self):
        v = ListValidator()
        self.assertEquals([], v.values)
        self.assertFalse(v.is_valid('foo'))

    def test_valid(self):
        v = ListValidator(['a', 'b', 'c'])
        self.assertTrue(v.is_valid('a'))
        self.assertFalse(v.is_valid('foo'))

    def test_validCaseSensitive(self):
        v = ListValidator(['A', 'b', 'C'])
        self.assertTrue(v.is_valid('a'))
        self.assertTrue(v.is_valid('B'))


if __name__ == '__main__':
    unittest.main()