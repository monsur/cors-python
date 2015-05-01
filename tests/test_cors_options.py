import unittest

from cors import validators
from cors import cors_options


class TestCorsOptions(unittest.TestCase):

    def test_defaultInstance(self):
        o = cors_options.CorsOptions()
        self.assertTrue(
          isinstance(o.origin_validator, validators.BooleanValidator)
        )
        self.assertEquals(cors_options.ALL_ORIGINS, o.origin_value)
        self.assertTrue(
          isinstance(o.methods_validator, validators.ListValidator)
        )
        self.assertEquals(cors_options.DEFAULT_METHODS, o.methods_value)
        self.assertTrue(
          isinstance(o.headers_validator, validators.BooleanValidator)
        )
        self.assertIsNone(o.headers_value)
        self.assertEquals([], o.expose_headers)
        self.assertFalse(o.allow_credentials)
        self.assertTrue(o.vary)
        self.assertIsNone(o.max_age)

    def test_originsList(self):
        o = cors_options.CorsOptions(allow_origins=['http://foo.com'])
        self.assertTrue(
          isinstance(o.origin_validator, validators.ListValidator)
        )
        self.assertIsNone(o.origin_value)
        self.assertTrue(o.vary)

    def test_allowCredentials(self):
        o = cors_options.CorsOptions(allow_credentials=True)
        self.assertTrue(o.allow_credentials)

    def test_exposeHeaders(self):
        o = cors_options.CorsOptions(expose_headers=['Header1'])
        self.assertEquals(['Header1'], o.expose_headers)

    def test_maxAge(self):
        o = cors_options.CorsOptions(max_age=1200)
        self.assertEquals(1200, o.max_age)

    def test_invalidMaxAge(self):
        try:
            _ = cors_options.CorsOptions(max_age='foo')
        except:
            return
        self.fail('Expected TypeError')

    def test_allowMethods(self):
        o = cors_options.CorsOptions(allow_methods=['foo'])
        self.assertTrue(
          isinstance(o.methods_validator, validators.ListValidator)
        )
        self.assertEquals(['foo'], o.methods_value)

    def test_allowAllMethods(self):
        o = cors_options.CorsOptions(allow_methods=True)
        self.assertTrue(
          isinstance(o.methods_validator, validators.BooleanValidator)
        )
        self.assertIsNone(o.methods_value)

    def test_allowHeaders(self):
        o = cors_options.CorsOptions(allow_headers=['foo'])
        self.assertTrue(
          isinstance(o.headers_validator, validators.ListValidator)
        )
        self.assertEquals(['foo'], o.headers_value)

    def test_allowAllHeaders(self):
        o = cors_options.CorsOptions(allow_headers=True)
        self.assertTrue(
          isinstance(o.headers_validator, validators.BooleanValidator)
        )
        self.assertIsNone(o.headers_value)


if __name__ == '__main__':
    unittest.main()
