from errors import NonCorsRequestError
from filter import Filter


class AllowNonCorsRequestFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if not self.options.allow_non_cors_requests:
            return NonCorsRequestError()
