from cors_exception import AllowOriginException
from filter import Filter


class AllowOriginFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        origin = request.origin
        is_valid_origin = self.options.origin_validator.is_valid(origin)
        if not is_valid_origin:
            return AllowOriginException(origin)
        response.allow_origin = self.get_origin_value(origin)

    def get_origin_value(self, origin):
        origin_value = self.options.origin_value
        if (self.options.allow_credentials or
             not origin_value) and not self.options.continue_on_error:
            origin_value = origin
        return origin_value



