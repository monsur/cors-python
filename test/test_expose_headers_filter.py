import unittest
from cors_options import CorsOptions
from cors_response import CorsResponse
from expose_headers_filter import ExposeHeadersFilter


class TestExposeHeadersFilter(unittest.TestCase):

    def test_noHeader(self):
        options = CorsOptions()
        response = CorsResponse()
        f = ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(0, len(response.expose_headers))

    def test_addHeader(self):
        options = CorsOptions(expose_headers=["Foo"])
        response = CorsResponse()
        f = ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(1, len(response.expose_headers))
        self.assertEquals('Foo', response.expose_headers[0])


if __name__ == '__main__':
    unittest.main()
