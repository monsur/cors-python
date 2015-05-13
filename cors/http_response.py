import httplib

from cors import constants


class ResponseState(object):
    """Indicates how the response should behave."""

    END = 1  # The response should end. Do not pass go. Do not collect $200.
    CONTINUE = 2  # The response should continue to the downstream handlers.


class HttpResponse(object):
    """Stores the CORS-specific response details.

    This class contains any response headers that should be set on the response
    as well as a state property, which indicates whether the request should
    continue or end. If the response ends, the status property indicates the
    recommended HTTP status code for the response.
    """
    def __init__(self):
        self.headers = {}
        self.state = ResponseState.CONTINUE
        # '200 OK'
        self.status = '%s %s' % (httplib.OK, httplib.responses[httplib.OK])
        self.error = None

    def end(self, error=None):
        if error:
            self.status = error.status
            self.error = error
        self.state = ResponseState.END


def create(request, response, error=None):
    """Creates a new HttpResponse instance.

    Args:
      request (CorsRequest) - The request details.
      response (CorsResponse) - The response details.
      error (CorsException) - The error (if any). Defaults to None.
    """
    http_response = HttpResponse()

    # Set any generic response headers (such as Vary).
    for key, value in response.headers.items():
        http_response.headers[key] = value

    if error:
        # If there is an error, return immediately, do not set any
        # CORS-specific headers.
        http_response.end(error)
        return http_response

    # The Access-Control-Allow-Origin and Access-Control-Allow-Credentials are
    # set on both CORS and preflight responses.
    if response.allow_origin:
        http_response.headers[constants.ACCESS_CONTROL_ALLOW_ORIGIN] = \
            response.allow_origin
    if response.allow_credentials:
        http_response.headers[constants.ACCESS_CONTROL_ALLOW_CREDENTIALS] = \
            'true'

    if request.is_preflight:
        # Set the preflight-only headers.
        if len(response.allow_methods):
            http_response.headers[constants.ACCESS_CONTROL_ALLOW_METHODS] = \
                ','.join(response.allow_methods)
        if response.allow_headers and len(response.allow_headers):
            http_response.headers[constants.ACCESS_CONTROL_ALLOW_HEADERS] = \
                ','.join(response.allow_headers)
        if response.max_age:
            http_response.headers[constants.ACCESS_CONTROL_MAX_AGE] = \
                str(response.max_age)
        # '200 OK'
        http_response.status = '%s %s' % (
            httplib.OK,
            httplib.responses[httplib.OK]
        )
        http_response.end()
    else:
        # Set the CORS-only headers.
        if len(response.expose_headers):
            http_response.headers[constants.ACCESS_CONTROL_EXPOSE_HEADERS] = \
                ','.join(response.expose_headers)
    return http_response
