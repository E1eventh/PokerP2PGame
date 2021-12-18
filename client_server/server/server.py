from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from queue import Queue
from random import randint
import xmlrpc.client

peers = Queue()
game_size = 4
is_running = True
addr = ("127.0.0.1", 50505)


def register(address):
    try:
        address = address[0] + ':' + str(address[1])
        peers.put(address)
        print(f"Players in queue: {peers.qsize()}")
    except:
        return False

    try:
        if peers.qsize() >= game_size:
            create_game()
    except:
        return False

    return True


def create_game():
    temp = []

    for i in range(game_size):
        temp.append(peers.get())

    seed = randint(0, 12345)
    balance = 1000

    for i in temp:
        addr = 'http://' + i
        print(addr)
        proxy = xmlrpc.client.ServerProxy(addr)
        proxy.start(seed, balance, temp)


def ping():
    return True


if __name__ == "__main__":
    server = SimpleXMLRPCServer(addr, requestHandler=SimpleXMLRPCRequestHandler, allow_none=True, logRequests=False)
    server.register_function(register)
    server.register_function(ping)

    try:
        server.serve_forever()
    except:
        print('Shut down')
