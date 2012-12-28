import unittest
from cors_options import CorsOptions
from cors_response import CorsResponse
from allow_credentials_filter import AllowCredentialsFilter


class TestAllowCredentialsFilter(unittest.TestCase):

    def test_addHeader(self):
        options = CorsOptions(allow_credentials=True)
        response = CorsResponse()
        f = AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertTrue(response.allow_credentials)

    def test_noHeader(self):
        options = CorsOptions(allow_credentials=False)
        response = CorsResponse()
        f = AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertFalse(response.allow_credentials)


if __name__ == '__main__':
    unittest.main()
