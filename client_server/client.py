from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import ServerProxy

import xmlrpc.client
import threading
import traceback
import time

# sys.path.insert(0, '../../')
from client_server.sharedData import SharedData

class Client:
    address = None
    saddress = None
    is_shutdown = False
    server_started = 0
    server = None
    data = SharedData()

    def __init__(self, local_address, server_address) -> None:
        self.address = local_address
        self.saddress = server_address


    # Close application
    def close(self):
        print("Shutting down")
        self.is_shutdown = True
        if self.server is not None:
            proxy = ServerProxy("http://" + self.address[0] + ":" + str(self.address[1]))
            # send last request to iterate request handle loop
            proxy.ping()


    def server_handler(self):
        try:
            self.server = SimpleXMLRPCServer(self.address, requestHandler=SimpleXMLRPCRequestHandler,
                                        allow_none=True, logRequests=False)

            self.server.register_instance(self.data)
            # server.register_function(ping)
            self.server_started = 1
            while not self.is_shutdown:
                self.server.handle_request()
        except:
            print(traceback.format_exc())
            self.server_started = -1

        # print("я закрылся")

    def __start_server(self):
        server_thread = threading.Thread(target=self.server_handler)
        server_thread.start()


    def start(self):
        self.__start_server()
        while not self.server_started:
            time.sleep(0.5)

        if self.server_started == -1:
            print("Could not start local server")
            self.close()
            return None

        proxy = None
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
                    proxy.ping()
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
