from urllib.parse import unquote

from context.request import Request
from context.response import Response
from consts import constants
import os


class MyHandler:
    def read_file(self, path):
        with open(path, 'rb') as f:
            body = f.read()
        return body

    def handle(self, sock):
        bytes = b''
        while not bytes.endswith(b'\n'):
            bytes += sock.recv(1024)

        data = bytes.decode()
        print(data)
        request = Request(data)

        if request.method not in constants.ALLOWED_METHODS:
            self.create_response(constants.STATUS_NOT_ALLOWED, sock)
            return

        if not request.ok:
            self.create_response(constants.STATUS_BAD_RESPONSE, sock)
            return

        if '/../' in request.path:
            self.create_response(constants.STATUS_FORBIDDEN, sock)
            return

        request.path = unquote(request.path.split('?')[0])

        request.path = os.getcwd() + request.path
        if os.path.isdir(request.path):
            request.path += 'index.html'
            if not os.path.isfile(request.path):
                self.create_response(constants.STATUS_FORBIDDEN, sock)
        try:
            body = self.read_file(request.path)
        except Exception:
            self.create_response(constants.STATUS_NOTFOUND, sock)
            return

        self.create_response(constants.STATUS_OK, sock, body, request.path, request.method)

    def create_response(self, status, sock, body='', path='', method=''):
        resp = Response()
        resp.set_status(status)

        if status == constants.STATUS_OK:
            resp.set_params(body, path, method)

        resp.generate_headers()
        sock.sendall(resp.encode())
