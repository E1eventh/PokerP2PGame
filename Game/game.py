from random import seed, shuffle

from Table.table import Table


class Game:
    def __init__(self, game_seed: int, players: list[str], balance: int):
        # seed(game_seed)
        self.table = Table(players, balance, shuffle)
        self.bets = {player_id: 0 for player_id in players}

    def game_initialization(self):
        self.deal()
        self.flop()
        self.turn()
        self.river()

    def deal(self):
        for i in range(2):
            for player in self.table.players.values():
                player.receive_card(self.table.deck.pop_card_from_deck())

    def flop(self):
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        for i in range(3):
            # Выкладывание карты на стол
            self.table.board.append(self.table.deck.pop_card_from_deck())

    def turn(self):
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def river(self):
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def check(self):
        pass

    def fold(self):
        pass

    def call(self):
        pass

    def bet_raise(self):
        pass



if __name__ == '__main__':
    for j in range(10):
        game = Game(10, ['192.168.0.1:80', '192.168.0.2:80', '192.168.0.3:80', '192.168.0.4:80'], 1000)
        game.game_initialization()

        for player in game.table.players.values():
            cards_list = player.hand
            print([(card.value, card.suit) for card in cards_list])

        board_cards_list = game.table.board
        print([(card.value, card.suit) for card in board_cards_list])

        print(len(game.table.deck.current_deck))
