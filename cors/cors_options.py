"""Options for configuring the CORS handler."""

import types
import validators


ALL_ORIGINS = '*'
DEFAULT_METHODS = ['HEAD', 'GET', 'PUT', 'POST', 'DELETE']


class CorsOptions(object):
    """Stores options for configuring the CORS handler."""

    def __init__(self,
                 allow_origins=True,
                 allow_credentials=False,
                 allow_methods=None,
                 allow_headers=True,
                 expose_headers = None,
                 max_age=None,
                 vary=None,
                 allow_non_cors_requests=True,
                 continue_on_error=False):
        """
        allow_origins (Validator) - The origins that are allowed. Set to True to
        allow all origins, or to a list of valid origins. Defaults to True, which
        allows all origins, and appends the Access-Control-Allow-Origin: * response
        header.

        allow_credentials (bool) - Whether or not the app supports credentials. If
        True, appends the Access-Control-Allow-Credentials: true header. Defaults to
        False.

        allow_methods (Validator) - The HTTP methods that are allowed. Set to True
        to allow all methods, or to a list of allowed methods. Defauts to ['HEAD',
        'GET', 'PUT', 'POST', 'DELETE'], which appends the
        Access-Control-Allow-Methods: HEAD, GET, PUT, POST, DELETE response header.

        allow_headers (Validator) - The HTTP request headers that are allowed. Set
        to True to allow all headers, or to a list of allowed headers. Defaults to
        True, which appends the Access-Control-Allow-Headers response header.

        expose_headers (list of strings) - List of response headers to expose to the
        client. Defaults to None. Appends the Access-Control-Expose-Headers response
        header.

        max_age (int) - The maximum time (in seconds) to cache the preflight
        response. Defaults to None, which doesn't append any response headers.
        Appends the Access-Control-Max-Age header when set.

        vary (bool) - Set to True if the Vary: Origin header should be appended to
        the response, False otherwise. The Vary header is useful when used in
        conjunction with a list of valid origins, and tells downstream proxy servers
        not to cache the response based on Origin. The default value is False for
        '*' origins, True otherwise.

        allow_non_cors_requests (bool) - Whether non-CORS requests should be
        allowed. Defaults to True.

        continue_on_error (bool) - Whether an invalid CORS request should trigger an
        error, or continue processing. Defaults to False.
        """
        self.origin_validator = validators.create(allow_origins)

        if allow_methods is None:
            allow_methods = DEFAULT_METHODS
        self.methods_validator = validators.create(allow_methods)

        if allow_headers is None:
            allow_headers = []
        self.headers_validator = validators.create(allow_headers)

        self.allow_credentials = allow_credentials

        if expose_headers is None:
            expose_headers = []
        self.expose_headers = expose_headers

        if max_age and not isinstance(max_age, types.IntType):
            raise TypeError('max_age must be an int.')
        self.max_age = max_age

        # The *_value properties below are the actual values to use in the
        # Access-Control-Allow-* headers. Set to None if the value is based
        # on the request and cannot be precalculated. Otherwise these values are
        # set now.

        # Only set the origin value if it is '*', since that is the only option
        # that can be precalculated (The actual origin value depends on the
        # request).
        self.origin_value = None
        if allow_origins == True:
            self.origin_value = ALL_ORIGINS

        # Only set the methods and headers if they are a list. If they are a
        # list, the entire list is returned in the preflight response. If they
        # are not a list (bool, regex, funciton, etc), then the request values
        # are echoed back to the user (and the values below are set to None
        # since they can't be precalculated).
        self.methods_value = None
        if isinstance(allow_methods, types.ListType):
            self.methods_value = allow_methods

        self.headers_value = None
        if isinstance(allow_headers, types.ListType):
            self.headers_value = allow_headers

        if vary is None:
            if self.origin_value == ALL_ORIGINS:
                vary = False
            else:
                vary = True
        self.vary = vary

        self.allow_non_cors_requests = allow_non_cors_requests
        self.continue_on_error = continue_on_error
