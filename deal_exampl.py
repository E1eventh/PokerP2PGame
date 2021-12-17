from game.game import Game
from deal.deal import Deal

if __name__ == '__main__':
    game = Game(10, ['192.168.0.1:80', '192.168.0.2:80', '192.168.0.3:80', '192.168.0.4:80'], 1000)

    for i in range(2):

        game.start_new_deal()

