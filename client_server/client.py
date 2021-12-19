from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import ServerProxy
from timeit import default_timer

import xmlrpc.client
import threading
import traceback
import time

from client_server.sharedData import SharedData


class Client:
    """Класс клиента игрока"""
    def __init__(self, local_address, server_address):
        """
        Конструктор объектов класса клиента игрока
        :param local_address: локальный адрес клиента
        :param server_address: адрес сервера
        """
        # Свойства
        self._is_shutdown = False
        self._server_started = 0
        self._server = None

        # Атрибуты
        self.data = SharedData()
        self.address = local_address
        self.saddress = server_address

    @property
    def is_shutdown(self):
        """Getter атрибута is_shutdown"""
        return self._is_shutdown

    @is_shutdown.setter
    def is_shutdown(self, flag):
        """Setter атрибута is_shutdown"""
        self._is_shutdown = flag

    @property
    def server_started(self):
        """Getter атрибута server_started"""
        return self._server_started

    @server_started.setter
    def server_started(self, server_started_status):
        """Setter атрибута server_started"""
        self._server_started = server_started_status

    @property
    def server(self):
        """Getter атрибута server"""
        return self._server

    @server.setter
    def server(self, server_object):
        """Setter атрибута server"""
        self._server = server_object

    def close(self):
        """Метод закрытия приложения"""
        print("Shutting down")
        self.is_shutdown = True

        if self.server is not None:
            proxy = ServerProxy("http://" + self.address[0] + ":" + str(self.address[1]))

            # send last request to iterate request handle loop
            proxy.ping()

    def server_handler(self):
        """Метод, регистрирующий сервер"""
        try:
            self.server = SimpleXMLRPCServer(self.address, requestHandler=SimpleXMLRPCRequestHandler,
                                        allow_none=True, logRequests=False)

            self.server.register_instance(self.data)
            self.server_started = 1

            while not self.is_shutdown:
                self.server.handle_request()
        except:
            print(traceback.format_exc())
            self.server_started = -1

    def __start_server(self):
        """Метод, стартующий сервер"""
        server_thread = threading.Thread(target=self.server_handler)
        server_thread.start()

    def start(self):
        """Метод, стартующий приложение"""
        self.__start_server()
        while not self.server_started:
            time.sleep(0.5)

        if self.server_started == -1:
            print("Could not start local server")
            self.close()
            return None

        try:
            proxy = xmlrpc.client.ServerProxy(f'http://{self.saddress}')
            proxy.register(self.address)
        except:
            print("No connection to signal server")
            self.close()
            return None

        try:
            while not self.data.is_playing:
                try:
                    ping_time = default_timer()
                    proxy.ping()
                    print(f"Время, затрачиваемое на проверку соездинения с сервером: {default_timer() - ping_time}")
                    time.sleep(1)
                except:
                    print('Connection lost')
                    self.close()
                    return None
        except KeyboardInterrupt:
            print('Bye')
            self.close()
            return None

        return self.data
