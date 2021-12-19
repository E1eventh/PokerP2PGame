class Deal:
    """Класс игровой раздачи"""
    def __init__(self, players: list[str]):
        """
        Конструктор класса игровой раздачи
        :param players: идентификаторы игроков в порядке хода
        """
        # Порядок хода игроков
        self.players_order = players
        # Ставки игроков
        self.players_bet = {player: 0 for player in players}
        # Указатель на игрока, который делает ход
        self.player_pointer = 0
        # Количество игроков, завершивших ход
        self.finished_turn_players = 0

    def move_pointer(self):
        """Метод, передвигающий указатель очерёдности хода"""
        self.player_pointer += 1
        if self.player_pointer > len(self.players_order) - 1:
            self.player_pointer = 0

    def is_all_players_finished(self):
        """Метод, возВращающий True, если все игроки завершили ход"""
        return self.finished_turn_players == len(self.players_order)

    def set_player_bet(self, player_id, bet_size):
        """
        Метод, устанавливающий ставку, введённую игроком
        :param player_id: id игрока
        :param bet_size: размер ставки
        """
        self.players_bet[player_id] = bet_size

    def get_player_bet(self, player_id):
        """
        Метод, возвращающий ставку, сделанную игроком
        :param player_id: id игрока
        :return: размер ставки игрока
        """
        return self.players_bet[player_id]

    def get_max_bet(self):
        """Метод, возвращающий макимальную ставку за столом"""
        return max(self.players_bet.values())
