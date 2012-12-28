# cors-python

A server-side CORS implementation for Python. This library is currently under
construction and is a very pre-alpha release. Testing and feedback welcome!


# Installation

Nothing fancy for now, just copy the cors/ directory over.

# Usage

See the app engine app under the "examples" directory for a sample usage.

For WSGI-compatible apps, you can wrap you application with the
cors_application.py middleware:

    webapp = webapp2.WSGIApplication([('/', MainHandler)])
    corsapp = CorsApplication(webapp, CorsOptions())

The CorsOptions class accepts the following properties:

_allow\_origins_ (Validator) - The origins that are allowed. Set to True to allow
all origins, or to a list of valid origins. Defaults to True, which allows all
origins, and appends the `Access-Control-Allow-Origin: *` response header.

_allow\_credentials_ (bool) - Whether or not the app supports credentials. If
True, appends the `Access-Control-Allow-Credentials: true` header. Defaults to
False.

_allow\_methods_ (Validator) - The HTTP methods that are allowed. Set to True to
allow all methods, or to a list of allowed methods. Defauts to ['HEAD', 'GET',
'PUT', 'POST', 'DELETE'], which appends the
`Access-Control-Allow-Methods: HEAD, GET, PUT, POST, DELETE` response header.

_allow\_headers_ (Validator) - The HTTP request headers that are allowed. Set to
True to allow all headers, or to a list of allowed headers. Defaults to True,
which appends the `Access-Control-Allow-Headers` response header.

_expose\_headers_ (list of strings) - List of response headers to expose to the
client. Defaults to None. Appends the `Access-Control-Expose-Headers` response
header.

_max\_age_ (int) - The maximum time (in seconds) to cache the preflight response.
Defaults to None, which doesn't append any response headers. Appends the
`Access-Control-Max-Age` header when set.

_vary_ (bool) - Set to True if the `Vary: Origin` header should be appended to
the response, False otherwise. The `Vary` header is useful when used in
conjunction with a list of valid origins, and tells downstream proxy servers
not to cache the response based on Origin. The default value is False for '*'
origins, True otherwise.

_allow\_non\_cors\_requests_ (bool) - Whether non-CORS requests should be
allowed. Defaults to True.

_continue\_on\_error_ (bool) - Whether an invalid CORS request should trigger
an error, or continue processing. Defaults to False.

## Validators

A few options above are marked as the special type "Validator". This type is
used to validate the origin, http method, and header values. The actual type
of the property can be set to various values, depending on the need:

* Boolean: A value of True indicates that all values are allowed. A value
of False indicates that no value is allowed.

* List of strings: The list of valid values. For example, the default list of
HTTP methods is ['HEAD', 'GET', 'PUT', 'POST', 'DELETE'].

* Regex (coming soon) - A regular expression to validate the value. Could be
useful for validating a set of subdomains (i.e. http://.*\.foo\.com) or custom
headers (i.e. x-prefix-.*)

* Function (coming soon) - Allows you to write your own function to validate the
input.

# Integrating with your own app

If the WSGI middleware does not meet your needs, you can always integrate with
the CORS library by writing your own handler. Your handler should call the
CorsHandler class in order to do the heavy lifting. See
[cors_application.py](https://github.com/monsur/cors-python/blob/master/cors/cors_application.py)
for an example of how to integrate with this library.
