from queue import Queue, Empty
from xmlrpc.client import ServerProxy
import time

class SharedData:
    def __init__(self):
        self._seed = 0
        self._balance = 0
        self._players = []
        self._is_playing = False
        self.queue = Queue()
        self.tries = 2

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, new_seed):
        self._seed = new_seed

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, new_players):
        self._players = new_players

    @property
    def is_playing(self):
        return self._is_playing

    @is_playing.setter
    def is_playing(self, new_status):
        self._is_playing = new_status

    def ping(self):
        return True


    def start(self, seed, balance, players):
        self.seed = seed
        self.balance = balance
        self.players = players
        self.is_playing = True

        print('start game')

        print(self.seed)
        print(self.balance)
        print(self.players)

    def put_action(self, action):
        self.queue.put(action)
        return True

    def send_action(self, action, player_id):
        res = []
        for player in self.players:
            if player == player_id:
                continue
            for i in range(self.tries):
                try:
                    proxy = ServerProxy(f"http://{player}")
                    proxy.put_action(action)
                    res.append(True)
                    break
                except Exception as ex:
                    if i < self.tries:
                        time.sleep(1)
                        continue
                    else:
                        res.append(False)
                        print(str(ex))
        return res

    def get_action(self, player_id):
        while True:
            try:
                res = self.queue.get(timeout=10)
            except Empty as empty:
                try:
                    proxy = ServerProxy(f"http://{player_id}")
                    proxy.ping()
                    continue
                except:
                    return f"delete {player_id}"
            return res
