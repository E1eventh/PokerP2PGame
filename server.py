from client_server.server import Server

if __name__ == "__main__":
  server = Server(50505, 4)
  server.start()
