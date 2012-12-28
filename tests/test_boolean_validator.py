from boolean_validator import BooleanValidator
import unittest


class TestBooleanValidator(unittest.TestCase):

  def test_true(self):
    true_validator = BooleanValidator(True)
    self.assertTrue(true_validator.is_valid('random value'))

  def test_false(self):
    false_validator = BooleanValidator(False)
    self.assertFalse(false_validator.is_valid('random value'))


if __name__ == '__main__':
    unittest.main()