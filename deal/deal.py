class Deal:
    """Класс игровой раздачи"""
    def __init__(self, players: list[str]):
        """
        Конструктор класса игровой раздачи
        :param players: идентификаторы игроков в порядке хода
        """
        # Переменные для property
        self._is_round_end = False
        self._is_deal_end = False

        # Атрибуты
        # Порядок хода игроков
        self.players_order = players
        # Статус игрока, True - сходил, False - не сходил
        self.players_status = [False] * len(players)

    @property
    def is_round_end(self):
        return self._is_round_end

    @is_round_end.setter
    def is_round_end(self, round_status):
        self._is_round_end = round_status

    @property
    def is_deal_end(self):
        return self._is_deal_end

    @is_deal_end.setter
    def is_deal_end(self, deal_status):
        self._is_deal_end = deal_status

    def delete_player_from_deal(self, player_id):
        self.players_order.remove(player_id)
