class CorsError(Exception):
    """Base exception for all CORS-related errors."""

    def __init__(self, status='500 Internal Server Error'):
        Exception.__init__(self, status)
        self.status = status


class OriginError(CorsError):
    """Invalid request origin."""

    def __init__(self, origin):
        CorsError.__init__(self, '403 Forbidden')
        self.origin = origin

    def __str__(self):
        return 'Disallowed origin: %s' % self.origin


class MethodError(CorsError):
    """Invalid request method."""

    def __init__(self, request_method):
        CorsError.__init__(self, '405 Method Not Allowed')
        self.request_method = request_method

    def __str__(self):
        return 'HTTP method %s not allowed.' % self.request_method


class HeadersError(CorsError):
    """Invalid request header(s)."""

    def __init__(self, invalid_headers):
        CorsError.__init__(self, '403 Forbidden')
        self.invalid_headers = invalid_headers

    def __str__(self):
        return 'Headers not allowed: %s' % ','.join(self.invalid_headers)


class NonCorsRequestError(CorsError):
    """Non-cors request (if non-cors requests are disabled)."""

    def __init__(self):
        CorsError.__init__(self, '400 Bad Request')

    def __str__(self):
        return 'Non-CORS requests not allowed'