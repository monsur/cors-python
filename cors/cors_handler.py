import filters
import http_response
from cors_response import CorsResponse
from cors_request import CorsRequest


class CorsHandler:

    def __init__(self, options):
        self._filters = filters.Filters(options)

    def handle(self, http_method=None, headers=None):
        request = CorsRequest(http_method, headers)
        response = CorsResponse()

        error = self._filters.run(request, response)

        return http_response.create(request, response, error)
