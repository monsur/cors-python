import unittest
from cors import constants
from cors import cors_handler


class TestCorsRequest(unittest.TestCase):

    def test_defaultInstance(self):
        req = cors_handler.CorsRequest()
        self.assertIsNone(req.http_method)
        self.assertIsNone(req.origin)
        self.assertIsNone(req.request_method)
        self.assertIsNone(req.request_headers)
        self.assertFalse(req.is_cors)
        self.assertFalse(req.is_preflight)

    def test_setMethod(self):
        req = cors_handler.CorsRequest('GET')
        self.assertEquals('GET', req.http_method)

    def test_headers(self):
        headers = {}
        headers[constants.ORIGIN] = 'http://github.com'
        headers[constants.ACCESS_CONTROL_REQUEST_METHOD] = 'GET'
        headers[constants.ACCESS_CONTROL_REQUEST_HEADERS] = 'Header1, Header2'
        req = cors_handler.CorsRequest('GET', headers)

        self.assertEquals('http://github.com', req.origin)
        self.assertEquals('GET', req.request_method)
        self.assertEquals(['Header1', 'Header2'], req.request_headers)

    def test_isCors(self):
        headers = {}
        headers[constants.ORIGIN] = 'http://github.com'
        req = cors_handler.CorsRequest('GET', headers)
        self.assertTrue(req.is_cors)
        self.assertFalse(req.is_preflight)

    def test_isPreflight(self):
        headers = {}
        headers[constants.ORIGIN] = 'http://github.com'
        headers[constants.ACCESS_CONTROL_REQUEST_METHOD] = 'PUT'
        req = cors_handler.CorsRequest('OPTIONS', headers)
        self.assertTrue(req.is_cors)
        self.assertTrue(req.is_preflight)

    def test_notPreflight1(self):
        headers = {}
        headers[constants.ORIGIN] = 'http://github.com'
        headers[constants.ACCESS_CONTROL_REQUEST_METHOD] = 'PUT'
        req = cors_handler.CorsRequest('GET', headers)
        self.assertTrue(req.is_cors)
        self.assertFalse(req.is_preflight)

    def test_notPreflight2(self):
        headers = {}
        headers['Origin'] = 'http://github.com'
        req = cors_handler.CorsRequest('OPTIONS', headers)
        self.assertTrue(req.is_cors)
        self.assertFalse(req.is_preflight)


if __name__ == '__main__':
    unittest.main()
