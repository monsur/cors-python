from errors import AllowHeadersError
from filter import Filter


class AllowHeadersFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        request_headers = request.request_headers
        if not request_headers:
            return
        if not len(request_headers):
            return

        valid = []
        not_valid = []
        for header in request_headers:
            if self.options.headers_validator.is_valid(header):
                valid.append(header)
            else:
                not_valid.append(header)

        headers_value = self.options.headers_value

        if len(not_valid):
            response.allow_headers = headers_value
            return AllowHeadersError(not_valid)

        if not headers_value:
            headers_value = valid
        response.allow_headers = headers_value
