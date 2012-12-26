import unittest
from cors_options import CorsOptions
from cors_response import CorsResponse
from max_age_filter import MaxAgeFilter


class TestMaxAgeFilter(unittest.TestCase):

    def test_noHeader(self):
        options = CorsOptions()
        response = CorsResponse()
        f = MaxAgeFilter(options)
        f.filter(None, response)
        self.assertIsNone(response.max_age)

    def test_addHeader(self):
        options = CorsOptions(max_age=1000)
        response = CorsResponse()
        f = MaxAgeFilter(options)
        f.filter(None, response)
        self.assertEquals(1000, response.max_age)


if __name__ == '__main__':
    unittest.main()
