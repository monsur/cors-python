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
                if key == 'origin':
                    self.origin = value
                elif key == 'access-control-request-method':
                    self.request_method = value
                elif key == 'access-control-request-headers':
                    self.request_headers = [x.strip() for x in value.split(',')]

        # Detect whether the request is a CORS or preflight request.
        if self.origin:
            # If this request has an Origin, it is a CORS request.
            self.is_cors = True
            if (self.http_method == 'OPTIONS' and
                self.request_method is not None):
                # If this is an OPTIONS request with an
                # Access-Contro-Request-Method header, its a preflight.
                self.is_preflight = True