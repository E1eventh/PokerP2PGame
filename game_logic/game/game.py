"""System module."""
from random import seed, shuffle

from game_logic.table.table import Table
from game_logic.deal.deal import Deal
from client_server.sharedData import SharedData


class Game:
    """Класс игры"""
    def __init__(self, current_player_id: str, data: SharedData):
        """
        Конструктор класса игры
        :param game_seed: seed для псевдорандомного генератора
        :param players: список игроков
        :param balance: начальный баланс игроков
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
        self.big_blind = int(data.balance / 100)
        self.small_blind = int(self.big_blind / 2)
        # Минимальная возможная ставка
        self.min_bet = self.big_blind

    def start_new_deal(self):
        """Начало новой раздачи"""
        # Удаляем ссылку на предудщий экземпляр класса раздачи
        del self.deal

        self.table.move_players_order()
        self.table.delete_bankrupts()

        # Создаём новую раздачу
        self.deal = Deal(self.table.players_order)

    def preflop(self):
        """Раздача карт игрокам"""
        self.deal.set_player_bet(self.deal.players_order[self.deal.player_pointer], self.small_blind)
        self.table.players[self.deal.players_order[self.deal.player_pointer]].change_bankroll(-self.small_blind)
        self.deal.move_pointer()
        self.deal.set_player_bet(self.deal.players_order[self.deal.player_pointer], self.big_blind)
        self.table.players[self.deal.players_order[self.deal.player_pointer]].change_bankroll(-self.big_blind)
        self.deal.move_pointer()

        for i in range(2):
            for player in self.table.players.values():
                player.receive_card(self.table.deck.pop_card_from_deck())

    def flop(self):
        """Выкладывание на стол первых трёх карт"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Установка минимальной ставки
        self.min_bet = self.big_blind

        for i in range(3):
            # Выкладывание карты на стол
            self.table.board.append(self.table.deck.pop_card_from_deck())

    def turn(self):
        """Выкладывание на стол четвёртой карты"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Установка минимальной ставки
        self.min_bet = self.big_blind

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def river(self):
        """Выкладывание на стол пятой карты"""
        # Сброс карты
        self.table.deck.pop_card_from_deck()

        # Установка минимальной ставки
        self.min_bet = self.big_blind

        # Выкладывание карты на стол
        self.table.board.append(self.table.deck.pop_card_from_deck())

    def fold(self, player_id):
        """
        Сброс своей руки игроком
        :param player_id: идентификатор игрока
        """
        self.table.players[player_id].set_empty_hand()
        # TODO: fix this
        self.table.delete_the_player(self.table.players[player_id])

    def check(self):
        """Пропуск ставки игроком"""
        self.deal.finished_turn_players += 1

    def bet(self, player_id, bet_size):
        """
        Ставка игрока
        :param player_id: идентификатор игрока
        :param bet_size: размер ставки
        """
        # Изменяем возможную минимальную ставку
        self.min_bet = bet_size
        # Увиличиваем банк нна размер ставки
        self.table.increase_bank(bet_size)
        # Вычитаем сумму ставки из банкролла игрока
        self.table.players[player_id].change_bankroll(-bet_size)
        self.deal.set_player_bet(player_id, bet_size)

    def call(self, player_id, bet_size):
        """
        Ставка игрока
        :param player_id: идентификатор игрока
        :param bet_size: размер ставки
        """
        # Изменяем возможную минимальную ставку
        self.min_bet = bet_size
        # Увиличиваем банк нна размер ставки
        self.table.increase_bank(bet_size)
        # Вычитаем сумму ставки из банкролла игрока
        self.table.players[player_id].change_bankroll(-bet_size)
        # Увиличиваем количество сходивших игроков
        self.deal.finished_turn_players += 1
        self.deal.set_player_bet(player_id, bet_size)

    def delete_bankrupts(self):
        """Удаляем банкротов из игры"""
        for player in self.table.players:
            if player.is_bankrupt:
                self.table.delete_the_player(player)


    def betting_round(self):
        while not self.deal.is_finished_betting_round():
            current_player = self.deal.players_order[self.deal.player_pointer]

            # Я хожу или другой игрок?
            my_turn = current_player == self.current_player_id

            # Переменные для обработки хода, заполняются дальше
            player_action = ''
            player_bet = 0
            # Нужно ли сдвигать  очердь хода?
            # Вообще нужно, если удалили игрока, то другая логика
            is_move_ptr = True

            print(f"Current number of players: {len(self.table.players)}")
            # Print the hand
            print(f'board: {[(card.value, card.suit) for card in self.table.board]}')
            
            # Получение данных о ходе
            # Из ввода, если хожу я
            # От другого клиента, если хожу не я
            if my_turn:
                print(f'Hand: {[(card.value, card.suit) for card in self.table.players[current_player].hand]}')
                print(f'Minimum bet: {max(self.deal.players_bet.values())}')
                print(f'your bank: {self.table.players[current_player].bankroll}')
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
            method_with_args = ""
            if player_action == 'call':
                self.call(current_player, player_bet)
                method_with_args = f'call {current_player} {player_bet}'
            elif player_action == 'raise':
                self.bet(current_player, player_bet)
                method_with_args = f'bet {current_player} {player_bet}'
            elif player_action == 'fold':
                self.fold(current_player)
                method_with_args = f'fold {current_player}'
            elif player_action == 'check':
                self.check()
                method_with_args = f'check'
            elif player_action == 'delete':
                is_move_ptr = self.table.delete_the_player(current_player)
                method_with_args = f'delete {current_player}'

            # Посылаем всем, если мой ход
            if my_turn:
                self.data.send_action(method_with_args, current_player)
            if is_move_ptr:
                self.deal.move_pointer()

        self.deal.finished_turn_players = 0

        return len(self.table.players_order) > 1
