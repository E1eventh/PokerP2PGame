from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from queue import Queue
from random import randint
import xmlrpc.client


class Server:
    peers = Queue()
    game_size = 4
    is_running = True
    addr = ("127.0.0.1", 50505)
    server = None

    def __init__(self, port: int) -> None:
        addr = ("127.0.0.1", port)


    def register(self, address):
        try:
            address = address[0] + ':' + str(address[1])
            self.peers.put(address)
            print(f"Players in queue: {self.peers.qsize()}")
        except:
            return False

        try:
            if self.peers.qsize() >= self.game_size:
                self.create_game()
        except:
            return False

        return True


    def create_game(self):
        temp = []

        for i in range(self.game_size):
            temp.append(self.peers.get())

        seed = randint(0, 12345)
        balance = 1000

        for i in temp:
            addr = 'http://' + i
            print(addr)
            proxy = xmlrpc.client.ServerProxy(addr)
            proxy.start(seed, balance, temp)


    def ping(self):
        return True


    def start(self):
        self.server = SimpleXMLRPCServer(self.addr, 
            requestHandler=SimpleXMLRPCRequestHandler, allow_none=True,
            logRequests=False)
        self.server.register_function(self.register)
        self.server.register_function(self.ping)

        try:
            self.server.serve_forever()
        except:
            print('Shut down')
