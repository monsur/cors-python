import types
import validators


ALL_ORIGINS = '*'
DEFAULT_METHODS = ['HEAD', 'GET', 'PUT', 'POST', 'DELETE']


class CorsOptions:

    def __init__(self,
                 allow_origins=True,
                 allow_credentials=False,
                 expose_headers = None,
                 max_age=None,
                 allow_methods=None,
                 allow_headers=None,
                 vary=None,
                 allow_non_cors_requests=True,
                 continue_on_error=False):
        self.allow_non_cors_requests = allow_non_cors_requests
        self.continue_on_error = continue_on_error
        self.origin_validator = validators.create(allow_origins)
        self.origin_value = None
        if allow_origins == True:
            self.origin_value = ALL_ORIGINS

        if vary is None:
            if self.origin_value == ALL_ORIGINS:
                vary = False
            else:
                vary = True
        self.vary = vary

        if allow_methods is None:
            allow_methods = DEFAULT_METHODS
        self.methods_validator = validators.create(allow_methods)
        self.methods_value = None
        if isinstance(allow_methods, types.ListType):
            self.methods_value = allow_methods

        if allow_headers is None:
            allow_headers = []
        self.headers_validator = validators.create(allow_headers)
        self.headers_value = None
        if isinstance(allow_headers, types.ListType):
            self.headers_value = allow_headers

        self.allow_credentials = allow_credentials

        if expose_headers is None:
            expose_headers = []
        self.expose_headers = expose_headers

        if max_age and not isinstance(max_age, types.IntType):
            raise TypeError('max_age must be an int.')
        self.max_age = max_age
