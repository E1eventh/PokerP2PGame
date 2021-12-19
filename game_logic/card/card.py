class Card:
    """Класс карты"""
    def __init__(self, value: int, suit: str):
        """
        Конструктор класса карты
        :param value: достоинство карты
        :param suit: масть карты
        """
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        """Метод для сортировки по достоинству карт"""
        return self.value <= other.value
