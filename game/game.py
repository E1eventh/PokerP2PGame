"""System module."""
from random import seed, shuffle

from table.table import Table
from deal.deal import Deal


class Game:
    """Класс игры"""
    def __init__(self, game_seed: int, players: list[str], balance: int):
        """
        Конструктор класса игры
        :param game_seed: seed для псевдорандомного генератора
        :param players: список игроков
        :param balance: начальный баланс игроков
        """
        seed(game_seed)
        self.table = Table(players, balance, shuffle)
        self.deal = Deal(players)
        self.bets = {player_id: 0 for player_id in players}
        self.big_blind = int(balance / 100)
        self.small_blind = int(self.big_blind / 2)

    def start_new_deal(self):
        """Начало новой раздачи"""
        # Удаляем ссылку на предудщий экземпляр класса раздачи
        del self.deal

        self.table.move_players_order()
        self.table.delete_bankrupts()

        # Создаём новую раздачу
        self.deal = Deal(self.table.players_order)

    def preflop(self):
        """Раздача карт игрокам"""
        for i in range(2):
            for player in self.table.players.values():
                player.receive_card(self.table.deck.pop_card_from_deck())

    def flop(self):
        """Выкладывание на стол первых трёх карт"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        self.table.players[self.deal.players_order[0]].change_bankroll(self.small_blind)
        self.deal.players_status[0] = True
        self.table.players[self.deal.players_order[0]].change_bankroll(self.big_blind)
        self.deal.players_status[1] = True

        for i in range(3):
            # Выкладывание карты на стол
            self.table.board.append(self.table.deck.pop_card_from_deck())

    def turn(self):
        """Выкладывание на стол четвёртой карты"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def river(self):
        """Выкладывание на стол пятой карты"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def fold(self, player_id):
        """
        Сброс своей руки игроком
        :param player_id: идентификатор игрока
        """
        self.table.players[player_id].set_empty_hand()
        self.table.delete_the_player(self.table.players[player_id])

    def check(self, player_id):
        """
        Пропуск ставки игроком
        :param player_id: идентификатор игрока
        """
        pass

    def bet(self, player_id, bet_size):
        """
        Ставка игрока
        :param player_id: идентификатор игрока
        :param bet_size: размер ставки
        """
        self.table.increase_bank(bet_size)
        self.table.players[player_id].change_bankroll(-bet_size)

    def delete_bankrupts(self):
        """Удаляем банкротов из игры"""
        for player in self.table.players:
            if player.is_bankrupt:
                self.table.delete_the_player(player)

    def betting_round(self):
        for i, player in enumerate(self.deal.players_order):
            pass
