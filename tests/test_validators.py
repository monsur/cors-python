import unittest
import validators


class TestValidators(unittest.TestCase):

    def test_create(self):
        self.subtest_create(validators.BooleanValidator, True)
        self.subtest_create(validators.BooleanValidator, False)
        self.subtest_create(validators.ListValidator, [])

        try:
            cors.validators.create({})
            self.fail('Expected exception')
        except Exception:
            return


    def subtest_create(self, t, v):
        self.assertTrue(isinstance(validators.create(v), t))


class TestBooleanValidator(unittest.TestCase):

  def test_true(self):
    true_validator = validators.BooleanValidator(True)
    self.assertTrue(true_validator.is_valid('random value'))

  def test_false(self):
    false_validator = validators.BooleanValidator(False)
    self.assertFalse(false_validator.is_valid('random value'))


class TestListValidator(unittest.TestCase):

    def test_emptyList(self):
        v = validators.ListValidator()
        self.assertEquals([], v.values)
        self.assertFalse(v.is_valid('foo'))

    def test_valid(self):
        v = validators.ListValidator(['a', 'b', 'c'])
        self.assertTrue(v.is_valid('a'))
        self.assertFalse(v.is_valid('foo'))

    def test_validCaseSensitive(self):
        v = validators.ListValidator(['A', 'b', 'C'])
        self.assertTrue(v.is_valid('a'))
        self.assertTrue(v.is_valid('B'))


if __name__ == '__main__':
    unittest.main()