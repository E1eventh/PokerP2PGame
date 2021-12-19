from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from random import randint

import xmlrpc.client


class Server:
    """Класс регистрационного сервера"""
    def __init__(self, port: int, players_in_game: int = 4):
        """
        Конструктор класса сервера
        :param port: порт
        :param players_in_game: количество игроков на одну комнату
        """
        # Свойства
        self._peers = []
        self._server = None

        # Атрибуты
        self.addr = ("127.0.0.1", port)
        self.game_size = players_in_game

    @property
    def peers(self):
        """Getter атрибута peers"""
        return self._peers

    @peers.setter
    def peers(self, new_peer):
        """Setter атрибута peers"""
        self._peers = new_peer

    @property
    def server(self):
        """Getter атрибута server"""
        return self._server

    @server.setter
    def server(self, new_server):
        """Setter атрибута server"""
        self._server = new_server

    def register(self, address):
        """Метод регистрации клиентов"""
        try:
            if len(self.peers) > 0:
                self.check_queue()

            address = address[0] + ':' + str(address[1])
            self.peers.append(address)

            print(f"Players in queue: {len(self.peers)}")
            print(self.peers)
        except:
            return False

        try:
            if len(self.peers) >= self.game_size:
                self.create_game()
        except:
            return False

        return True

    def check_queue(self):
        """Метод, проверящий очередь на наличие игроков и добавляющий их в пул готовых играть"""
        temp = []
        for i in self.peers:
            try:
                proxy = xmlrpc.client.ServerProxy("http://" + i)
                proxy.ping()
                # time.sleep(1)
            except:
                print('Connection with ' + i + ' lost')
                temp.append(i)

        self.peers = [i for i in self.peers if not i in temp]

    def create_game(self):
        """Метод, создающий игру"""
        temp = []

        for i in range(self.game_size):
            temp.append(self.peers[0])
            del self.peers[0]

        seed = randint(0, 12345)
        balance = 1000

        for i in temp:
            addr = 'http://' + i
            print(addr)
            proxy = xmlrpc.client.ServerProxy(addr)
            proxy.start(seed, balance, temp)

    def ping(self):
        """Метод возвращает True, если к серверу есть подключение"""
        return True

    def start(self):
        """Метод, стартующий сервер"""
        self.server = SimpleXMLRPCServer(self.addr, requestHandler=SimpleXMLRPCRequestHandler,
                                         allow_none=True, logRequests=False)
        self.server.register_function(self.register)
        self.server.register_function(self.ping)

        try:
            self.server.serve_forever()
        except:
            print('Shut down')
