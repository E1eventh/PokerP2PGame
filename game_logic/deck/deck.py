from collections.abc import Callable

from game_logic.card.card import Card


class Deck:
    """Класс колоды карт"""
    def __init__(self, shuffle_func: Callable):
        """
        Конструктор объектов класса колоды карт
        :param shuffle_func: функция для перемешивания карт в колоде
        """
        # Свойства
        self._current_deck = []

        # Атрибуты
        self.shuffle_func = shuffle_func
        self.update_deck()

    # Атрибуты
    @property
    def current_deck(self):
        """Getter атрибута current_deck"""
        return self._current_deck

    @current_deck.setter
    def current_deck(self, new_deck: list[Card]):
        """Setter атрибута current_deck"""
        self._current_deck = new_deck

    # Методы
    def __shuffle_deck(self):
        """Метод, возвращающий перемешанную колоду карт"""
        new_deck = [Card(value, suit) for suit in ['H', 'D', 'C', 'S'] for value in range(2, 15)]
        self.shuffle_func(new_deck)
        return new_deck

    def update_deck(self):
        """Метод, создающий новую перемешанную колоду карт"""
        self.current_deck = self.__shuffle_deck()

    def pop_card(self):
        """Метод, удаляющий и возвращающий верхнюю карту из колоды"""
        return self.current_deck.pop(0)
