"""
Definition of API exceptions that are used throughout the codebase.
"""


class WebServiceError(Exception):
    def __init__(self, reason=None, code=400):
        self.reason = reason
        self.code = code


class NotFound(WebServiceError):
    def __init__(self, reason=''):
        self.reason = reason
        self.code = 404


class ServerError(WebServiceError):
    def __init__(self):
        super(ServerError, self).__init__(
            reason='The server encountered an unexpected condition'
                   'that prevented it from fulfilling the request.',
            code=500
        )
