from filter import Filter


class AllowCredentialsFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.allow_credentials:
            response.allow_credentials = True
