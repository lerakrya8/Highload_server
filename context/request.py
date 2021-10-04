import logging

class Request:
    def __init__(self, data):
        self.data = data

        self.method = None
        self.ok = False
        self.path = None

        self.headers = {}

        self.parse()

    def parse(self):
        headers = self.data.split('\r\n')
        if len(headers) == 0:
            return

        self.method, self.path, _ = headers[0].split()

        for header in headers[1:]:
            if len(header.split(': ')) == 2:
                key, value = header.split(': ')
                self.headers[key] = value

        self.ok = True
