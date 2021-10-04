from urllib.parse import unquote

from context.request import Request
from context.response import Response
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

        if request.method not in ['GET', 'HEAD']:
            resp = Response()
            resp.set_status('405 NotAllowed')
            resp.generate_headers()
            sock.sendall(resp.encode())
            return

        if not request.ok:
            resp = Response()
            resp.set_status('400 Bad Response')
            resp.generate_headers()
            sock.sendall(resp.encode())
            return

        if '/../' in request.path:
            resp = Response()
            resp.set_status('403 Forbidden')
            resp.generate_headers()
            sock.sendall(resp.encode())
            return

        print(request.path)
        request.path = unquote(request.path.split('?')[0])
        print(request.path)

        request.path = os.getcwd() + request.path
        if os.path.isdir(request.path):
            request.path += 'index.html'
            if not os.path.isfile(request.path):
                resp = Response()
                resp.set_status('403 Forbidden')
                resp.generate_headers()
                sock.sendall(resp.encode())

        try:
            body = self.read_file(request.path)
        except Exception:
            resp = Response()
            resp.set_status('404 NotFound')
            resp.generate_headers()
            sock.sendall(resp.encode())
            return

        resp = Response()
        resp.set_status('200 OK')
        resp.set_params(body, request.path, request.method)
        resp.generate_headers()
        sock.sendall(resp.encode())