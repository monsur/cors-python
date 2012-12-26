from cors.boolean_validator import BooleanValidator
from cors.list_validator import ListValidator
import cors.validators
import unittest


class TestValidators(unittest.TestCase):

    def test_create(self):
        self.subtest_create(BooleanValidator, True)
        self.subtest_create(BooleanValidator, False)
        self.subtest_create(ListValidator, [])

        try:
            cors.validators.create({})
            self.fail('Expected exception')
        except Exception:
            return


    def subtest_create(self, t, v):
        self.assertTrue(isinstance(cors.validators.create(v), t))


if __name__ == '__main__':
    unittest.main()