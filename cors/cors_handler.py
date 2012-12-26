import http_response
from cors_exception import CorsException
from cors_response import CorsResponse
from cors_request import CorsRequest
from filters import Filters


class CorsHandler:

    def __init__(self, options):
        self._filters = Filters(options)

    def handle(self, http_method=None, headers=None):
        request = CorsRequest(http_method, headers)
        response = CorsResponse()

        error = self._filters.run(request, response)

        return http_response.create(request, response, error)
