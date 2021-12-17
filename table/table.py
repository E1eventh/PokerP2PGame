from collections.abc import Callable

from player.player import Player
from deck.deck import Deck


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
        self.players_order = players
        self.deck = Deck(shuffle_func)
        self.bank = self.set_empty_bank()
        self.board = []

    @staticmethod
    def set_empty_bank():
        return 0

    def increase_bank(self, amount: int):
        self.bank += amount

    def move_players_order(self):
        self.players_order = self.players_order.insert(len(self.players_order) - 1, self.players_order.pop(0))

    def delete_the_player(self, player_index):
        del self.players[player_index]
        self.players_order.remove(player_index)

    def delete_bankrupts(self):
        for player in self.players.values():
            if player.is_bankrupt:
                self.delete_the_player(player)
