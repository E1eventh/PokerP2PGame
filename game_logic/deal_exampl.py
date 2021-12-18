from game.game import Game


if __name__ == '__main__':
    game = Game(10, ['192.168.0.1:80', '192.168.0.2:80', '192.168.0.3:80', '192.168.0.4:80'], 1000)

    # for i in range(2):
    for street in ['preflop', 'flop', 'turn', 'river']:
        print(street)
        game.__getattribute__(street)()
        game.betting_round()
    game.start_new_deal()
