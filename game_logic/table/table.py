from collections.abc import Callable

from game_logic.player.player import Player
from game_logic.deck.deck import Deck


class Table:
    """Класс игрового стола"""
    def __init__(self, players: list[str], start_player_balance: int, shuffle_func: Callable):
        """
        Конструктор класса игрового стола
        :param players:
        :param start_player_balance:
        :param shuffle_func:
        """
        self.players = {player: Player(start_player_balance) for player in players}
        # Отсортированный в порядке хода игроки
        self.players_order = players
        self.deck = Deck(shuffle_func)

        # Банк на столе
        self.bank = 0
        # Карты на столе
        self.board = []
        # Активный игрок
        self.active = {player: True for player in players}

    def increase_bank(self, amount: int):
        """Метод, увелдичивающий размер банка"""
        self.bank += amount

    def delete_the_player(self, player_index):
        """Метод, удаляющий из игры игрока, у которого закончился баланс"""
        need_move = False
        idx = self.players_order.index(player_index)

        if idx >= len(self.players_order) - 1:
            need_move = True

        self.players_order.remove(player_index)

        del self.active[player_index]
        del self.players[player_index]
        return need_move
