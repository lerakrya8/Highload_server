from server.handler import MyHandler

import socket
import os
import logging


class Server:
    def __init__(self, handler: MyHandler):
        self.handler = handler
        self.socket = None
        self.workers = []

        self.host = "0.0.0.0"
        self.port = 81
        self.limit_connection = 500
        self.limit_threads = 4

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tp = (self.host, self.port)
        self.socket.bind(tp)
        self.socket.listen(self.limit_connection)
        # logging.log('start listen socket')

        for thread in range(self.limit_threads):
            pid = os.fork()

            if pid != 0:
                self.workers.append(pid)
            else:
                while True:
                    connection, address = self.socket.accept()

                    try:
                        self.handler.handle(connection)
                    except Exception as exp:
                        logging.error(str(exp))

                    connection.close()

        for worker in self.workers:
            os.waitpid(worker, 0)
