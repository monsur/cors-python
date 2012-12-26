class CorsResponse(object):

    def __init__(self):
        self.allow_origin = None
        self.allow_credentials = False
        self.max_age = None
        self.expose_headers = []
        self.allow_methods = None
        self.allow_headers = None
        self.headers = {}
