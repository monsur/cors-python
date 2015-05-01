"""Processes a CORS request."""

from cors import constants
from cors import filters
from cors import http_response


class CorsHandler(object):
    """Processes a CORS request and returns the CORS response."""

    def __init__(self, options):
        self._filters = filters.Filters(options)

    def handle(self, http_method=None, headers=None):
        """Processes a CORS request and returns the CORS response.

        Returns an object with the HTTP headers to set on the response.
        """
        request = CorsRequest(http_method, headers)
        response = CorsResponse()

        error = self._filters.run(request, response)

        return http_response.create(request, response, error)


class CorsRequest(object):

    def __init__(self, http_method=None, headers=None):
        self.http_method = http_method
        self.origin = None
        self.request_method = None
        self.request_headers = None
        self.is_cors = False
        self.is_preflight = False

        self.headers = {}
        # Load CORS-specific headers.
        if headers:
            for key, value in headers.items():
                self.headers[key] = value
                key = key.lower()
                if key == constants.ORIGIN.lower():
                    self.origin = value
                elif key == constants.ACCESS_CONTROL_REQUEST_METHOD.lower():
                    self.request_method = value
                elif key == constants.ACCESS_CONTROL_REQUEST_HEADERS.lower():
                    self.request_headers = [
                      x.strip()
                      for x in value.split(',')
                    ]

        # Detect whether the request is a CORS or preflight request.
        if self.origin:
            # If this request has an Origin, it is a CORS request.
            self.is_cors = True
            if (self.http_method == 'OPTIONS' and
                    self.request_method is not None):
                # If this is an OPTIONS request with an
                # Access-Control-Request-Method header, its a preflight.
                self.is_preflight = True


class CorsResponse(object):

    def __init__(self):
        self.allow_origin = None
        self.allow_credentials = False
        self.max_age = None
        self.expose_headers = []
        self.allow_methods = None
        self.allow_headers = None
        self.headers = {}
