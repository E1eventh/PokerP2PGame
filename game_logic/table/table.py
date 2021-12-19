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
        self.players_order = players
        self.deck = Deck(shuffle_func)
        # Банк на столе
        self.bank = 0
        self.board = []
        self.active = {p:True for p in players}

    def increase_bank(self, amount: int):
        self.bank += amount

    def move_players_order(self):
        tmp = self.players_order.pop(0)
        self.players_order.append(tmp)

    def delete_the_player(self, player_index):
        need_move = False
        # ValueIndex exception
        idx = self.players_order.index(player_index)
        if idx >= len(self.players_order) - 1:
            need_move = True
        self.players_order.remove(player_index)
        del self.active[player_index]
        del self.players[player_index]
        return need_move

    def delete_bankrupts(self):
        for player in self.players.values():
            if player.is_bankrupt:
                self.delete_the_player(player)

    def is_active(self, player):
        return self.active[player]

    def set_active(self, player, val):
        self.active[player] = val
