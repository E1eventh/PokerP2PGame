from game_logic.card.card import Card


class Player:
    """Класс игрока"""
    def __init__(self, bankroll: int):
        """Конструктор объектов класса игрока"""
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
        """Getter атрибута hand"""
        return self._hand

    @hand.setter
    def hand(self, new_hand: list[Card]):
        """Setter атрибута hand"""
        self._hand = new_hand

    @property
    def is_bankrupt(self):
        """Getter атрибута is_bankrupt"""
        return self._is_bankrupt

    @is_bankrupt.setter
    def is_bankrupt(self, bankrupt_flag: bool):
        """Setter атрибута is_bankrupt"""
        self._is_bankrupt = bankrupt_flag

    # Методы
    def set_empty_hand(self):
        """Метод, обнуляющий руку игрока"""
        self.hand = []

    def receive_card(self, card: Card):
        """
        Метод, добавляющий переданную карту в руку игрока
        :param card: переданная карта
        """
        new_hand = self.hand
        new_hand.append(card)
        self.hand = new_hand

    def change_bankroll(self, bankroll: int):
        """
        Метод, менящий банкролл игрока
        :param bankroll: сумма, на которую меняется банкролл игрока
        """
        if self.bankroll + bankroll > 0:
            self.bankroll += bankroll
        else:
            self.bankroll = 0
