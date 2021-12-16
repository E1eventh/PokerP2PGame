from collections.abc import Callable

from Player.player import Player
from Deck.deck import Deck


class Table:
    def __init__(self, players: list[str], start_player_balance: int, shuffle_func: Callable):
        self.players = {player: Player(start_player_balance) for player in players}
        self.players_order = players
        self.deck = Deck(shuffle_func)
        self.bank = self.set_empty_bank()
        self.board = []

    @staticmethod
    def set_empty_bank():
        return 0

    def move_players_order(self):
        self.players_order = self.players_order.insert(len(self.players_order) - 1, self.players_order.pop(0))

    def delete_the_player(self, player_index):
        self.players_order.remove(player_index)

    def delete_bankrupts(self):
        # Realizovat' pozhe
        # Запросить все индексы банкротов и для каждого вызвать delete_the_player
        pass

    def increase_bank(self, amount: int):
        self.bank += amount

