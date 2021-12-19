from xmlrpc import client

import sys
import traceback

from client_server.client import Client
from game_logic.game.game import Game

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Example: python сlient.py <port_number>")
    exit()
  address = ('127.0.0.1', int(sys.argv[1]))

  server_address = "127.0.0.1:50505"
  peer = Client(address, server_address)
  data = peer.start()

  if data is None:
    exit()

  
  print("Ready to play")


  try:
    # import sys, os
    # from pathlib import Path

    # from PySide6.QtQuick import QQuickView
    # from PySide6 import QtCore
    # from PySide6.QtGui import QGuiApplication, QIcon

    # class Console(QtCore.QObject):
    #     @QtCore.Slot(str)
    #     def outputStr(self, s):
    #         print(s)


    # app = QGuiApplication(sys.argv)
    # view = QQuickView()
    # view.setResizeMode(QQuickView.SizeRootObjectToView)

    # view.setMinimumWidth(900)
    # view.setMinimumHeight(600)

    # icon = QIcon("images/alice.jpg")
    # view.setIcon(icon)
    # view.setTitle("AlicePoker")

    # qml_file = os.path.join(os.path.dirname(__file__), 'mainWindow.qml')
    # view.setSource(QtCore.QUrl.fromLocalFile(os.path.abspath(qml_file)))

    # con = Console()
    # context = view.rootContext()
    # context.setContextProperty("con", con)

    # if view.status() == QQuickView.Error:
    #     sys.exit(-1)
    # view.show()

    # app.exec()
    # del view


    # TODO: pass only data object
    game = Game(data.seed, data.players, data.balance, f'{address[0]}:{address[1]}', data)

    for street in ['preflop', 'flop', 'turn', 'river']:
        print(street)
        game.__getattribute__(street)()
        game.betting_round()
    game.start_new_deal()
  except Exception as ex:
    print(str(ex))
    print(traceback.format_exc())
  finally:
    peer.close()
    print("END")
