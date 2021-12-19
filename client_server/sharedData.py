from xmlrpc.client import ServerProxy
from queue import Queue, Empty

import time


class SharedData:
    """Класс очереди"""
    def __init__(self):
        """Конструктор класса очереди"""
        # Свойства
        self._seed = 0
        self._balance = 0
        self._players = []
        self._is_playing = False

        # Атрибуты
        self.queue = Queue()
        self.tries = 2

    @property
    def seed(self):
        """Getter атрибута seed"""
        return self._seed

    @seed.setter
    def seed(self, new_seed):
        """Setter атрибута seed"""
        self._seed = new_seed

    @property
    def balance(self):
        """Getter атрибута balance"""
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        """Setter атрибута balane"""
        self._balance = new_balance

    @property
    def players(self):
        """Getter атрибута players"""
        return self._players

    @players.setter
    def players(self, new_players):
        """Setter атрибута players"""
        self._players = new_players

    @property
    def is_playing(self):
        """Getter атрибута is_playing"""
        return self._is_playing

    @is_playing.setter
    def is_playing(self, new_status):
        """Setter атрибута is_playing"""
        self._is_playing = new_status

    def ping(self):
        """Метод возвращает True, если к клиенту есть подключение"""
        return True

    def start(self, seed: int, balance: int, players: list[str]):
        """
        Метод стартующий подключение и игру
        :param seed: seed для генератора псевдорандома
        :param balance: начальный баланс игроков
        :param players: id игроков
        """
        self.seed = seed
        self.balance = balance
        self.players = players
        self.is_playing = True

        print('Start game')
        print(self.seed)
        print(self.balance)
        print(self.players)

    def put_action(self, action: str):
        """Метод для добавления действия игрока в очередь"""
        self.queue.put(action)
        return True

    def send_action(self, action: str, player_id: str):
        """Метод для отправки действия игрока другим игрокам"""
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

    def get_action(self, player_id: str):
        """Метод достающий из очереди действие другого игрока"""
        while True:
            try:
                res = self.queue.get(timeout=2)
            except Empty as empty:
                try:
                    proxy = ServerProxy(f"http://{player_id}")
                    proxy.ping()
                    continue
                except:
                    return f"delete {player_id}"
            return res
