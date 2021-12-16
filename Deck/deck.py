from collections.abc import Callable

from Card.card import Card


class Deck:
    def __init__(self, shuffle_func: Callable):
        self.shuffle_func = shuffle_func
        self._current_deck = []
        self.update_deck()

    # Атрибуты
    @property
    def current_deck(self):
        return self._current_deck

    @current_deck.setter
    def current_deck(self, new_deck: list[Card]):
        self._current_deck = new_deck

    # Методы
    @staticmethod
    def __shuffled_deck(shuffle_func: Callable):
        new_deck = [Card(value, suit) for suit in ['H', 'D', 'C', 'S'] for value in range(2, 15)]
        shuffle_func(new_deck)
        return new_deck

    def update_deck(self):
        self.current_deck = self.__shuffled_deck(self.shuffle_func)

    def pop_card_from_deck(self):
        return self.current_deck.pop(0)
