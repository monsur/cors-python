from cors_handler import CorsHandler
from http_response import ResponseState
import webob


class CorsApplication(object):

    def __init__(self, app, options=None):
        self._app = app
        self._handler = CorsHandler(options)

    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        response = request.get_response(self._app)
        cors_response = self._handler.handle(request.method, request.headers)

        status = str(cors_response.status)
        headers = cors_response.headers
        if cors_response.state == ResponseState.END:
            start_response(status, headers.items())
            return []
        else:
            for key, value in headers.items():
                response.headers.add(key, value)
            return response(environ, start_response)
