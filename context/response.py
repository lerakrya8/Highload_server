from time import strftime
from consts import config, constants


class Response:
    def __init__(self):
        self.headers = None
        self.body = None
        self.content_type = None
        self.content_length = 0
        self.status = None

    def generate_headers(self):
        if self.body is not None:
            self.content_length = len(self.body)
        self.headers = f"HTTP/1.1 {self.status}\r\n" + \
                       f"Server: {config.SERVER_NAME}\r\n" + \
                       f"Date: {strftime('%c')}\r\n" + \
                       f"Connection: keep-alive\r\n" + \
                       f"Content-Length: {self.content_length}\r\n" + \
                       f"Content-Type: {self.content_type}\r\n\r\n"

    def encode(self):
        if self.body is not None:
            return self.headers.encode() + self.body
        return self.headers.encode()

    def set_status(self, status):
        self.status = status

    def set_params(self, body, path, method):
        extension = path.split('.')[len(path.split('.')) - 1]
        if method != constants.METHOD_HEAD:
            self.body = body
        self.content_length = len(body)

        self.content_type = constants.CONTENT_TYPE.get(extension)
