class ResponseState(object):
    END = 1
    CONTINUE = 2


class HttpResponse(object):

    def __init__(self):
        self.headers = {}
        self.state = ResponseState.CONTINUE
        self.status = '200 OK'
        self.error = None

    def end(self, error=None):
        if error:
            self.status = error.status
            self.error = error
        self.state = ResponseState.END


def create(request, response, error):
    http_response = HttpResponse()

    for key, value in response.headers.items():
        http_response.headers[key] = value

    if error:
        http_response.end(error)
        return http_response

    if response.allow_origin:
        http_response.headers['Access-Control-Allow-Origin'] = \
            response.allow_origin
    if response.allow_credentials:
        http_response.headers['Access-Control-Allow-Credentials'] = \
            'true'

    if request.is_preflight:
        if len(response.allow_methods):
            http_response.headers['Access-Control-Allow-Methods'] = \
                ','.join(response.allow_methods)
        if response.allow_headers and len(response.allow_headers):
            http_response.headers['Access-Control-Allow-Headers'] = \
                ','.join(response.allow_headers)
        if response.max_age:
            http_response.headers['Access-Control-Max-Age'] = \
                str(response.max_age)
        http_response.status = '200 OK'
        http_response.end()
    else:
        if len(response.expose_headers):
            http_response.headers['Access-Control-Expose-Headers'] = \
                ','.join(response.expose_headers)

    return http_response
