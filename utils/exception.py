class ResponseException(Exception):
    payload = None
    status = "unknown_error"
    result = -1
    status_code = 500

    def __init__(self, payload=None, status='unknown_error', result=-1, status_code=500):
        self.payload = payload
        self.status = status
        self.result = result
        self.status_code = status_code

    def __str__(self):
        return repr(self.status)


class AccessDeniedException(ResponseException):
    status = 'access_denied'
    status_code = 403


class NotFoundException(ResponseException):
    def __init__(self):
        self.status = 'not_found'
        self.status_code = 404
