class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value <= other.value
