"""WSGI middleware for handling CORS requests."""

import webob

from cors import cors_handler
from cors import http_response


class CorsApplication(object):
    """WSGI middleware for handling CORS requests."""

    def __init__(self, app, options=None):
        self._handler = cors_handler.CorsHandler(options)
        self.app = app

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    def __call__(self, environ, start_response):
        # Retrieve the CORS response details.
        request = webob.Request(environ)
        cors_response = self.handler.handle(request.method, request.headers)

        headers = cors_response.headers
        if cors_response.state == http_response.ResponseState.END:
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
