"""System module."""
from random import seed, shuffle

from game_logic.table.table import Table
from game_logic.deal.deal import Deal
from client_server.sharedData import SharedData

from game_logic.combinations.combinations import get_strongest_combination


class Game:
    """Класс игры"""
    def __init__(self, current_player_id: str, data: SharedData):
        """
        Конструктор класса игры
        :param current_player_id: id текущего игрока
        :param data: клиентские данные для взаимодействия игроков
        """
        # Устанавливаем сид
        seed(data.seed)
        # Инициализируем стол
        self.table = Table(data.players, data.balance, shuffle)
        # id игрока
        self.current_player_id = current_player_id
        # Данные об игре
        self.data = data

        # Инициализируем раздачу
        self.deal = Deal(data.players)
        # Блайнды
        # self.big_blind = int(data.balance / 100)
        # self.small_blind = int(self.big_blind / 2)
        # Минимальная возможная ставка
        # self.min_bet = 0
        # self.min_bet = self.big_blind

    # def start_new_deal(self):
    #     """Начало новой раздачи"""
    #     # Удаляем ссылку на предудщий экземпляр класса раздачи
    #     del self.deal

    #     self.table.move_players_order()
    #     self.table.delete_bankrupts()

    #     # Создаём новую раздачу
    #     self.deal = Deal(self.table.players_order)

    # Phases
    def preflop(self):
        """Раздача карт игрокам"""
        # self.deal.set_player_bet(self.deal.get_current_player(), self.small_blind)
        # self.table.players[self.deal.get_current_player()].change_bankroll(-self.small_blind)
        # self.deal.move_pointer()
        # self.deal.set_player_bet(self.deal.get_current_player(), self.big_blind)
        # self.table.players[self.deal.get_current_player()].change_bankroll(-self.big_blind)
        # self.deal.move_pointer()

        # self.min_bet = 0

        for i in range(2):
            for player in self.table.players.values():
                player.receive_card(self.table.deck.pop_card())

    def flop(self):
        """Выкладывание на стол первых трёх карт"""
        # Сброс карты
        self.table.deck.pop_card()

        # Установка минимальной ставки
        # self.min_bet = 0

        for i in range(3):
            # Выкладывание карты на стол
            self.table.board.append(self.table.deck.pop_card())

    def turn(self):
        """Выкладывание на стол четвёртой карты"""
        # Сброс карты
        self.table.deck.pop_card()

        # Установка минимальной ставки
        # self.min_bet = 0

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card())

    def river(self):
        """Выкладывание на стол пятой карты"""
        # Сброс карты
        self.table.deck.pop_card()

        # Установка минимальной ставки
        # self.min_bet = 0

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card())

    # Actions
    def fold(self, player_id):
        """
        Сброс своей руки игроком
        :param player_id: идентификатор игрока
        """
        # self.table.players[player_id].set_empty_hand()
        # self.table.set_active(player_id, False)
        # self.table.delete_the_player()
        # TODO: fix this
        del self.deal.players_bet[player_id]
        return self.table.delete_the_player(player_id)

    def check(self, player_id):
        """Пропуск ставки игроком"""
        # TODO: check if player can check...
        if self.deal.get_max_bet() > self.deal.get_player_bet(player_id):
            # print("not checked")
            return False
        self.deal.finished_turn_players += 1
        # print("checked")
        return True

    def bet(self, player_id, bet_size):
        """
        Ставка игрока
        :param player_id: идентификатор игрока
        :param bet_size: размер ставки
        """
        # Изменяем возможную минимальную ставку
        # self.min_bet = bet_size
        # Увиличиваем банк нна размер ставки
        # self.table.increase_bank(bet_size)
        # Вычитаем сумму ставки из банкролла игрока
        # self.table.players[player_id].change_bankroll(-bet_size)
        if bet_size <= self.deal.get_max_bet():
            return False

        if self.table.players[player_id].bankroll < bet_size:
            return False

        self.deal.finished_turn_players = 1
        # print(f'BET: {bet_size}')
        self.deal.set_player_bet(player_id, bet_size)
        bet = self.deal.get_max_bet()
        # print(f'BET: {bet}')
        return True

    def call(self, player_id):
        """
        Ставка игрока
        :param player_id: идентификатор игрока
        :param bet_size: размер ставки
        """
        # Изменяем возможную минимальную ставку
        # self.min_bet = bet_size
        # Увиличиваем банк нна размер ставки
        # self.table.increase_bank(bet_size)
        # Вычитаем сумму ставки из банкролла игрока
        # self.table.players[player_id].change_bankroll(-bet_size)
        # Увеличиваем количество сходивших игроков

        self.deal.finished_turn_players += 1
        bet = self.deal.get_max_bet()
        player_bankroll = self.table.players[player_id].bankroll

        if bet <= 0:
            return False

        if player_bankroll < bet:
            bet = player_bankroll

        self.deal.set_player_bet(player_id, bet)
        return True

    def round_end(self):
        for player in self.deal.players_order:
            bet = self.deal.get_player_bet(player)
            self.deal.set_player_bet(player, 0)
            self.table.players[player].change_bankroll(-bet)
            self.table.increase_bank(bet)

        self.deal.player_pointer = 0

        return False


    def betting_round(self):
        while not self.deal.is_all_players_finished():
            if len(self.table.players) < 2:
                return 1

            current_player = self.deal.players_order[self.deal.player_pointer]

            # Я хожу или другой игрок?
            my_turn = current_player == self.current_player_id

            # Нужно ли сдвигать  очердь хода?
            # Вообще нужно, если удалили игрока, то другая логика
            is_move_ptr = True

            print(f"Current number of players: {len(self.table.players)}")
            print(f"MAX BET: {self.deal.get_max_bet()}")
            # Print the hand
            print(f'board: {[(card.value, card.suit) for card in self.table.board]}')

            # Сообщение, которое отправляем, а заодно и флаг
            method_with_args = ""
            while len(method_with_args) <= 0:
                # Получение данных о ходе
                # Из ввода, если хожу я
                # От другого клиента, если хожу не я
                if my_turn:
                    print("YOUR TURN!")
                    print(f'Hand: {[(card.value, card.suit) for card in self.table.players[current_player].hand]}')
                    print(f'Your bet: {self.deal.get_player_bet(current_player)}')
                    print(f'Your bank: {self.table.players[current_player].bankroll}')
                    player_move = input().split()
                    player_action = player_move[0]
                    player_bet = 0 if len(player_move) < 2 else int(player_move[1])
                else:
                    print(f"Waiting for player's action: {current_player}")
                    player_move = self.data.get_action(current_player).split()
                    player_action = player_move[0]
                    to_print = f"Player action: {player_action}"
                    args = player_move[1:]
                    player_bet = 0
                    if len(args) > 1:
                        args[1] = int(args[1])
                        player_bet = args[1]
                        to_print += f" {player_bet}"
                    print(to_print)


                # Обрабатываем ход
                if player_action == 'call':
                    if self.call(current_player):
                        method_with_args = f'call {current_player}'
                elif player_action == 'raise':
                    if self.bet(current_player, player_bet):
                        method_with_args = f'raise {current_player} {player_bet}'
                elif player_action == 'fold':
                    is_move_ptr = self.fold(current_player)
                    method_with_args = f'fold {current_player}'
                elif player_action == 'check':
                    if self.check(current_player):
                        method_with_args = f'check'
                        # print("double checked")
                elif player_action == 'delete':
                    is_move_ptr = self.table.delete_the_player(current_player)
                    method_with_args = f'delete {current_player}'
                else:
                    print("Wrong action. Try again.")

                # print("ACTION: {method_with_args}")

            # Посылаем всем, если мой ход
            if my_turn:
                # print("SENDING ACTION")
                self.data.send_action(method_with_args, current_player)

            # Если мы сфолдили, то мы все
            if self.current_player_id not in self.table.players:
                return -1

            if is_move_ptr:
                print("MOVING PTR")
                self.deal.move_pointer()

            print(f"POINTER: {self.deal.player_pointer}")

        if self.round_end():
            return -1

        self.deal.finished_turn_players = 0

        return len(self.table.players_order)

    def __players_combinations(self):
        players_combinations = {}

        for player in self.deal.players_order:
            players_cards = self.table.players[player].hand + self.table.board

            players_combinations[player] = get_strongest_combination(players_cards)

        return players_combinations

    def define_the_winner(self):
        players_combinations = self.__players_combinations()

        strongest_combination = max(players_combinations.values())

        for key, value in players_combinations.items():
            if value[0] < strongest_combination:
                del players_combinations[key]

        return players_combinations
