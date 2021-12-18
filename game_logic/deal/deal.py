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
        self.player_pointer += 1
        if self.player_pointer > len(self.players_order) - 1:
            self.player_pointer = 0

    def is_finished_betting_round(self):
        if self.finished_turn_players == len(self.players_order):
            return True
        return False

    def nullify_finished_turn_players(self):
        self.finished_turn_players = 0

    def is_all_players_finished_turn(self):
        return self.finished_turn_players == len(self.players_order)

    def set_player_bet(self, player_id, bet_size):
        self.players_bet[player_id] = bet_size

    def delete_player_from_deal(self, player_id):
        self.players_order.remove(player_id)
