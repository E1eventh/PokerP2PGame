from Card.card import Card


class Player:
    def __init__(self, bankroll: int):
        # Переменные для property
        self._is_bankrupt = False
        self._hand = []

        # Атрибуты
        self.bankroll = bankroll
        self.is_bankrupt = False

        # Инициализция руки
        self.set_empty_hand()

    # Атрибуты
    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, new_hand: list[Card]):
        self._hand = new_hand

    @property
    def is_bankrupt(self):
        return self._is_bankrupt

    @is_bankrupt.setter
    def is_bankrupt(self, bankrupt_flag: bool):
        self._is_bankrupt = bankrupt_flag

    # Методы
    def set_empty_hand(self):
        self.hand = []

    def set_player_bankrupt(self):
        self.is_bankrupt = True

    def receive_card(self, card: Card):
        new_hand = self.hand
        new_hand.append(card)
        self.hand = new_hand

    def change_bankroll(self, bankroll: int):
        self.bankroll += bankroll
