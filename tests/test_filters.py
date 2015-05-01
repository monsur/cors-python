import unittest
from cors import constants
from cors import errors
from cors import filters
from cors import cors_options
from cors import cors_handler


class TestAllowCredentialsFilter(unittest.TestCase):

    def test_addHeader(self):
        options = cors_options.CorsOptions(allow_credentials=True)
        response = cors_handler.CorsResponse()
        f = filters.AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertTrue(response.allow_credentials)

    def test_noHeader(self):
        options = cors_options.CorsOptions(allow_credentials=False)
        response = cors_handler.CorsResponse()
        f = filters.AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertFalse(response.allow_credentials)


class TestAllowNonCorsRequestFilter(unittest.TestCase):

    def test_allow(self):
        options = cors_options.CorsOptions(allow_non_cors_requests=True)
        f = filters.AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNone(error)

    def test_disallow(self):
        options = cors_options.CorsOptions(allow_non_cors_requests=False)
        f = filters.AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNotNone(error)


class TestAllowOriginFilter(unittest.TestCase):

    def test_allowAllOrigins(self):
        options = cors_options.CorsOptions()
        f = filters.AllowOriginFilter(options)

        # Test with no Origin
        request = cors_handler.CorsRequest()
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

        # Test CORS request
        request = cors_handler.CorsRequest(
          'GET',
          {
            constants.ORIGIN: 'http://foo.com'
          }
        )
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

        # Test CORS preflight request
        request = cors_handler.CorsRequest(
          'OPTIONS', {
            constants.ORIGIN: 'http://foo.com',
            constants.ACCESS_CONTROL_REQUEST_METHOD: 'GET'
          }
        )
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

    def test_invalidOrigin(self):
        options = cors_options.CorsOptions(allow_origins=['http://foo.com'])
        f = filters.AllowOriginFilter(options)
        request = cors_handler.CorsRequest(
          'GET',
          {
            constants.ORIGIN: 'http://bar.com'
          }
        )
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsInstance(error, errors.OriginError)
        self.assertIsNone(response.allow_origin)

    def test_validOrigin(self):
        options = cors_options.CorsOptions(allow_origins=['http://foo.com'])
        f = filters.AllowOriginFilter(options)
        request = cors_handler.CorsRequest(
          'GET',
          {
            constants.ORIGIN: 'http://foo.com'
          }
        )
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('http://foo.com', response.allow_origin)

    def test_allowCredentials(self):
        options = cors_options.CorsOptions(
          allow_origins=True,
          allow_credentials=True
        )
        f = filters.AllowOriginFilter(options)
        request = cors_handler.CorsRequest(
          'GET',
          {
            constants.ORIGIN: 'http://foo.com'
          }
        )
        response = cors_handler.CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('http://foo.com', response.allow_origin)


class TestExposeHeadersFilter(unittest.TestCase):

    def test_noHeader(self):
        options = cors_options.CorsOptions()
        response = cors_handler.CorsResponse()
        f = filters.ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(0, len(response.expose_headers))

    def test_addHeader(self):
        options = cors_options.CorsOptions(expose_headers=["Foo"])
        response = cors_handler.CorsResponse()
        f = filters.ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(1, len(response.expose_headers))
        self.assertEquals('Foo', response.expose_headers[0])


class TestMaxAgeFilter(unittest.TestCase):

    def test_noHeader(self):
        options = cors_options.CorsOptions()
        response = cors_handler.CorsResponse()
        f = filters.MaxAgeFilter(options)
        f.filter(None, response)
        self.assertIsNone(response.max_age)

    def test_addHeader(self):
        options = cors_options.CorsOptions(max_age=1000)
        response = cors_handler.CorsResponse()
        f = filters.MaxAgeFilter(options)
        f.filter(None, response)
        self.assertEquals(1000, response.max_age)


class TestVaryFilter(unittest.TestCase):

    def test_addHeader(self):
        options = cors_options.CorsOptions(vary=True)
        response = cors_handler.CorsResponse()
        filtr = filters.VaryFilter(options)
        filtr.filter(None, response)
        self.assertEquals(constants.ORIGIN, response.headers[constants.VARY])

    def test_noHeader(self):
        options = cors_options.CorsOptions(vary=False)
        response = cors_handler.CorsResponse()
        filtr = filters.VaryFilter(options)
        filtr.filter(None, response)
        self.assertFalse(constants.VARY in response.headers)


if __name__ == '__main__':
    unittest.main()
