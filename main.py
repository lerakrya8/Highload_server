from server import server
from server.handler import MyHandler


if __name__ == '__main__':
    print('hello')
    handler = MyHandler()

    server = server.Server(handler=handler)
    server.run()
    print('вышли')
