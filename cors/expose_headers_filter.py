from filter import Filter


class ExposeHeadersFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if len(self.options.expose_headers):
            response.expose_headers = self.options.expose_headers