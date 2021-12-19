import sys

from client_server.client import Client
from game_logic.game.game import Game


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Example: python сlient.py <port_number>")
        exit()

    address = ('127.0.0.1', int(sys.argv[1]))

    server_address = "127.0.0.1:50505"
    peer = Client(address, server_address)
    data = peer.start()

    if data is None:
        exit()

    print("Ready to play")

    try:
        game = Game(f'{address[0]}:{address[1]}', data)

        res = 0
        for street in ['preflop', 'flop', 'turn', 'river']:
            print(f'\n\n{street.capitalize()}')

            # Fill the board
            game.__getattribute__(street)()

            # Action
            res = game.betting_round()
            if res < 2:
                break

        if res < 0:
            print("You lose!")
        else:
            print("Winner:")

            winner = game.define_the_winner()
            print(winner)

            print(f'board: {[(card.value, card.suit) for card in game.table.board]}')
            tmp = list(winner.keys())[0]
            print(f'Hand: {[(card.value, card.suit) for card in game.table.players[tmp].hand]}')
    except KeyboardInterrupt as ki:
        print(str(ki))
    finally:
        peer.close()
        print("END")
