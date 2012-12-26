
from cors_options import CorsOptions
from cors_response import CorsResponse
from allow_non_cors_request_filter import AllowNonCorsRequestFilter
import unittest


class TestAllowNonCorsRequestFilter(unittest.TestCase):

    def test_allow(self):
        options = CorsOptions(allow_non_cors_requests=True)
        f = AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNone(error)

    def test_disallow(self):
        options = CorsOptions(allow_non_cors_requests=False)
        f = AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNotNone(error)


if __name__ == '__main__':
    unittest.main()
