from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.client import ServerProxy

import xmlrpc.client
import threading
import traceback
import sys
import time

# TODO:
sys.path.insert(0, '../../')
from game_logic.game.game import Game
from client_server.info import Info


address = None

# System variables
is_shutdown = False
server_started = 0
server = None

info = Info()


# Close application
def close():
    global is_shutdown
    print("Shutting down")
    is_shutdown = True
    if server is not None:
        proxy = ServerProxy("http://" + address[0] + ":" + str(address[1]))
        # send last request to iterate request handle loop
        proxy.ping()
    sys.exit()


def server_handler():
    global server_started, server
    try:
        server = SimpleXMLRPCServer(address, requestHandler=SimpleXMLRPCRequestHandler,
                                    allow_none=True, logRequests=False)

        server.register_instance(info)
        # server.register_function(ping)
        server_started = 1
        while not is_shutdown:
            server.handle_request()
    except:
        server_started = -1

    # print("я закрылся")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Example: python сlient.py <port_number>")
        close()
    address = ('127.0.0.1', int(sys.argv[1]))
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    while not server_started:
        time.sleep(0.5)

    if server_started == -1:
        print("Could not start local server")
        close()

    proxy = None
    try:
        proxy = xmlrpc.client.ServerProxy('http://127.0.0.1:50505')
        proxy.register(address)
    except:
        print("No connection to signal server")
        close()

    try:
        while not info.is_playing:
            try:
                proxy.ping()
                time.sleep(1)
            except:
                print('Connection lost')
                close()
    except KeyboardInterrupt:
        print('пока')
        close()

    print("сейчас будем играть но пока нет")

    # TODO: game logic
    game = Game(info.seed, info.players, info.balance, f'{address[0]}:{address[1]}', info)

    try:
        for street in ['preflop', 'flop', 'turn', 'river']:
            print(street)
            game.__getattribute__(street)()
            game.betting_round()
        game.start_new_deal()
    except Exception as ex:
        print(str(ex))
        print(print(traceback.format_exc()))
    finally:
        close()
