from errors import AllowOriginError
from filter import Filter


class AllowOriginFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        origin = request.origin
        is_valid_origin = self.options.origin_validator.is_valid(origin)

        origin_value = self.options.origin_value

        if not is_valid_origin:
            response.allow_origin = origin_value
            return AllowOriginError(origin)

        if (self.options.allow_credentials or
            not origin_value):
            origin_value = origin

        response.allow_origin = origin_value
