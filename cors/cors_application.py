"""WSGI middleware for handling CORS requests."""

import webob
from cors_handler import CorsHandler
from http_response import ResponseState


class CorsApplication(object):
    """WSGI middleware for handling CORS requests."""

    def __init__(self, app, options=None):
        self.app = app
        self.handler = CorsHandler(options)

    def __call__(self, environ, start_response):
        # Retrieve the CORS response details.
        request = webob.Request(environ)
        cors_response = self.handler.handle(request.method, request.headers)

        headers = cors_response.headers
        if cors_response.state == ResponseState.END:
            # Response should end immediately. Set the status and any headers
            # and exit.
            start_response(cors_response.status, headers.items())
            return []
        else:
            # Response should continue to the user's app. Set any CORS-specific
            # headers and keep going.
            response = request.get_response(self.app)
            for key, value in headers.items():
                response.headers.add(key, value)
            return response(environ, start_response)
