from filter import Filter


class VaryFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.vary:
            response.headers['Vary'] = 'Origin'
