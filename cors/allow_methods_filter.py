from errors import AllowMethodsError
from filter import Filter


class AllowMethodsFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        is_valid = self.options.methods_validator.is_valid(
            request.request_method)

        allow_methods = self.options.methods_value

        if not is_valid:
            response.allow_methods = allow_methods
            return AllowMethodsError(request.request_method)

        if not allow_methods:
            allow_methods = [request.request_method]
        response.allow_methods = allow_methods
