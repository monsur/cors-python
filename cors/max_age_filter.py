from filter import Filter


class MaxAgeFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.max_age:
            response.max_age = self.options.max_age
