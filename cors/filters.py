from allow_credentials_filter import AllowCredentialsFilter
from allow_headers_filter import AllowHeadersFilter
from allow_methods_filter import AllowMethodsFilter
from allow_non_cors_request_filter import AllowNonCorsRequestFilter
from allow_origin_filter import AllowOriginFilter
from cors_filter import CorsFilter
from expose_headers_filter import ExposeHeadersFilter
from max_age_filter import MaxAgeFilter
from vary_filter import VaryFilter


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

    def create_filters(self, all_filters, *args):
        filters = []
        for arg in args:
            filters.append(all_filters[arg])
        return filters

    def run(self, request, response):
        filters = self.choose_filters(request)
        for f in filters:
            error = f.filter(request, response)
            if error:
                return error
        return None

    def choose_filters(self, request):
        if request.is_preflight:
            return self.preflight_filters
        elif request.is_cors:
            return self.cors_filters
        else:
            return self.non_cors_filters
