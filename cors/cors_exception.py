class CorsException(Exception):

    def __init__(self, status=500):
        Exception.__init__(self, status)
        self.status = status


class AllowOriginException(CorsException):

    def __init__(self, origin):
        CorsException.__init__(self, 400)
        self.origin = origin

    def __str__(self):
        return 'Disallowed origin: %s' % self.origin


class AllowMethodsException(CorsException):

    def __init__(self, request_method):
        CorsException.__init__(self, 400)
        self.request_method = request_method

    def __str__(self):
        return 'HTTP method %s not allowed.' % self.request_method


class AllowHeadersException(CorsException):

    def __init__(self, invalid_headers):
        CorsException.__init__(self, 400)
        self.invalid_headers = invalid_headers

    def __str__(self):
        return 'Headers not allowed: %s' % ','.join(self.invalid_headers)


class NonCorsRequestException(CorsException):

    def __init__(self):
        CorsException.__init__(self, 400)

    def __str__(self):
        return 'Non-CORS requests not allowed'