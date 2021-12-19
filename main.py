from xmlrpc import client

import sys
import traceback

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
    
    # Убрать блайнды +
    # Fold - не падать - для игрока - конец игры (можно наблюдать)
    # Raise n - поднять свою ставку до n
    # Check - нельзя чекать, если твоя ставка не равна максимальной
    # Call - убрать аргументы - сравнивает текущую ставку с максимальной

    game = Game(f'{address[0]}:{address[1]}', data)

    res = 0
    for street in ['preflop', 'flop', 'turn', 'river']:
        print(f'\n\n{street.capitalize()}')

        print(f"Current bank: {game.table.bank}")
        
        # Fill the board
        game.__getattribute__(street)()

        # Print the board
        # for card in game.table.board:
        #   print(card.value, card.suit)
        
        # Action
        res = game.betting_round()
        if res < 0:
          break

    # TODO: print winner
    if res < 0:
      print("You lose!")
    else:
      print("Who won?")
    # game.start_new_deal()



    # while True:
    #   print("\n\nPreflop")
    #   game.preflop()
    #   res = game.betting_round
    #   if not res:
    #     break

    #   print("\n\nFlop")
    #   game.flop()
    #   res = game.flop()
    #   if not res:
    #     break

    #   print("\n\nTurn")
    #   game.turn()
    #   res = game.turn()
    #   if not res:
    #     break

    #   print("\n\nRiver")
    #   game.river()
    #   res = game.river()
    #   break


  except Exception as ex:
    print(str(ex))
    print(traceback.format_exc())
  finally:
    peer.close()
    print("END")
