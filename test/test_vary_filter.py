from cors_options import CorsOptions
from cors_response import CorsResponse
from vary_filter import VaryFilter
import unittest


class TestVaryFilter(unittest.TestCase):

    def test_addHeader(self):
        options = CorsOptions(vary=True)
        response = CorsResponse()
        filter = VaryFilter(options)
        filter.filter(None, response)
        self.assertEquals('Origin', response.headers['Vary'])

    def test_noHeader(self):
        options = CorsOptions(vary=False)
        response = CorsResponse()
        filter = VaryFilter(options)
        filter.filter(None, response)
        self.assertFalse('Vary' in response.headers)


if __name__ == '__main__':
    unittest.main()
