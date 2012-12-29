import errors


class Filters(object):

    def __init__(self, options):
        all_filters = {
            'allow_credentials': AllowCredentialsFilter(options),
            'allow_headers': AllowHeadersFilter(options),
            'allow_methods': AllowMethodsFilter(options),
            'allow_non_cors_request': AllowNonCorsRequestFilter(options),
            'allow_origin': AllowOriginFilter(options),
            'cors': CorsFilter(options),
            'expose_headers': ExposeHeadersFilter(options),
            'max_age': MaxAgeFilter(options),
            'vary': VaryFilter(options)
        }

        self.cors_filters = self.create_filters(all_filters,
                'vary',
                'allow_origin',
                'allow_credentials',
                'expose_headers')

        self.preflight_filters = self.create_filters(all_filters,
                'vary',
                'allow_origin',
                'allow_methods',
                'allow_headers',
                'allow_credentials',
                'max_age')

        self.non_cors_filters = self.create_filters(all_filters,
            'vary',
            'allow_non_cors_request')

        self.continue_on_error = options.continue_on_error

    def create_filters(self, all_filters, *args):
        filters = []
        for arg in args:
            filters.append(all_filters[arg])
        return filters

    def run(self, request, response):
        filters = self.choose_filters(request)
        for f in filters:
            error = f.filter(request, response)
            if error and not self.continue_on_error:
                return error
        return None

    def choose_filters(self, request):
        if request.is_preflight:
            return self.preflight_filters
        elif request.is_cors:
            return self.cors_filters
        else:
            return self.non_cors_filters


class Filter:

    def __init__(self, options):
        self.options = options


class AllowCredentialsFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.allow_credentials:
            response.allow_credentials = True


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
            return errors.AllowHeadersError(not_valid)

        if not headers_value:
            headers_value = valid
        response.allow_headers = headers_value


class AllowMethodsFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        is_valid = self.options.methods_validator.is_valid(
            request.request_method)

        allow_methods = self.options.methods_value

        if not is_valid:
            response.allow_methods = allow_methods
            return errors.AllowMethodsError(request.request_method)

        if not allow_methods:
            allow_methods = [request.request_method]
        response.allow_methods = allow_methods


class AllowNonCorsRequestFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if not self.options.allow_non_cors_requests:
            return errors.NonCorsRequestError()


class AllowOriginFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        origin = request.origin
        is_valid_origin = self.options.origin_validator.is_valid(origin)

        origin_value = self.options.origin_value

        if not is_valid_origin:
            response.allow_origin = origin_value
            return errors.AllowOriginError(origin)

        if (self.options.allow_credentials or
            not origin_value):
            origin_value = origin

        response.allow_origin = origin_value


class ExposeHeadersFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if len(self.options.expose_headers):
            response.expose_headers = self.options.expose_headers


class MaxAgeFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.max_age:
            response.max_age = self.options.max_age


class VaryFilter(Filter):

    def __init__(self, options):
        Filter.__init__(self, options)

    def filter(self, request, response):
        if self.options.vary:
            response.headers['Vary'] = 'Origin'

