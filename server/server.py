from server.handler import MyHandler
from consts import config

import socket
import os
import logging


class Server:
    def __init__(self, handler: MyHandler):
        self.handler = handler
        self.socket = None
        self.workers = []

        self.host = config.HOST
        self.port = config.PORT
        self.limit_connection = config.LIMIT_CONNECTIONS
        self.limit_forks = config.LIMIT_FORKS

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tp = (self.host, self.port)
        self.socket.bind(tp)
        self.socket.listen(self.limit_connection)

        for thread in range(self.limit_forks):
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
