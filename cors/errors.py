class CorsError(Exception):

    def __init__(self, status=500):
        Exception.__init__(self, status)
        self.status = status


class AllowOriginError(CorsError):

    def __init__(self, origin):
        CorsError.__init__(self, 400)
        self.origin = origin

    def __str__(self):
        return 'Disallowed origin: %s' % self.origin


class AllowMethodsError(CorsError):

    def __init__(self, request_method):
        CorsError.__init__(self, 400)
        self.request_method = request_method

    def __str__(self):
        return 'HTTP method %s not allowed.' % self.request_method


class AllowHeadersError(CorsError):

    def __init__(self, invalid_headers):
        CorsError.__init__(self, 400)
        self.invalid_headers = invalid_headers

    def __str__(self):
        return 'Headers not allowed: %s' % ','.join(self.invalid_headers)


class NonCorsRequestError(CorsError):

    def __init__(self):
        CorsError.__init__(self, 400)

    def __str__(self):
        return 'Non-CORS requests not allowed'