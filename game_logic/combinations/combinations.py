from game_logic.card.card import Card


def get_strongest_combination(cards: list[Card]):
    """
    Функция по поиску сильнейшей комбинации из набора переданных карт
    :param cards: набор карт
    :return: сильнейшая комбинация
    """
    return is_royal_flush(sorted(cards))


def is_flush_here(flush_cards: list[Card]):
    """
    Функция, проверяющая, что в наборе переданых карт есть флеш
    :param flush_cards: набор карт
    :return flush_cards: флаг наличия флеша
    :return suit: масть, формирующая флеш
    """
    suits = [card.suit for card in flush_cards]
    uniq_suits = list(set(suits))

    if len(uniq_suits) == 1:
        return True, uniq_suits[0]
    else:
        for uniq_suit in uniq_suits:
            if suits.count(uniq_suit) >= 5:
                return True, uniq_suit

    return False, ''


def is_straight_here(straight_cards: list[int]):
    """
    Функция, проверяющая, что в наборе переданных карт есть стрит
    :param straight_cards: набор карт
    :return straight_here:
    :return straight_here: флаг наличия стрита
    :return straight: карты, формирубщий стрит
    """
    smallest_straight = False
    straight_here = False
    straight = (0, 0)

    if len(straight_cards) < 5:
        return straight_here, straight

    if len(straight_cards) == 7:
        if straight_cards[6] - straight_cards[2] == 4:
            straight_here = True
            straight = (straight_cards[2], straight_cards[6])
        elif straight_cards[6] - straight_cards[3] == 9:
            smallest_straight = True
        straight_cards = straight_cards[:6]

    if len(straight_cards) == 6 and not straight_here:
        if straight_cards[5] - straight_cards[1] == 4:
            straight_here = True
            straight = (straight_cards[1], straight_cards[5])
        elif straight_cards[5] - straight_cards[3] == 9:
            smallest_straight = True
        straight_cards = straight_cards[:5]

    if straight_cards[4] - straight_cards[0] == 4 and not straight_here:
        straight_here = True
        straight = (straight_cards[0], straight_cards[4])
    elif straight_cards[4] - straight_cards[3] == 9:
        smallest_straight = True

    if not straight_here and smallest_straight:
        straight_here = True
        straight = (14, 5)

    return straight_here, straight


def is_some_of_a_kind_here(cards: list[Card], counter, excluded_card=None):
    """
    Функция, проверяющая, что в наборе переданных карт есть заданное
    число карт одного достоинства
    :param cards: набор карт
    :param counter: количество искомых карт одного достоинства
    :param excluded_card: карта, которую нужно исключить из набора карт
    :return some_of_a_kind_here: флаг наличия заданного числа карт одного достоинтсва
    :return value: достоинство карты, который содержитсся необходимое количество
    """
    cards_values = [card.value for card in cards if card.value != excluded_card]

    uniq_card_values = sorted(list(set(cards_values)))
    uniq_card_values.reverse()

    for uniq_card in uniq_card_values:
        if cards_values.count(uniq_card) == counter:
            return True, uniq_card

    return False, 0


def is_royal_flush(cards: list[Card]):
    """
    Проверка на наличии комбинации "Флеш Рояль" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    flush_here, flush_suit = is_flush_here(cards)
    possible_cards = [card.value for card in cards if card.suit == flush_suit]

    if flush_here:
        if sorted(possible_cards)[:-6:-1] == list(range(14, 9, -1)):
            return [9, 'Royal Flush', flush_suit]

    return is_straight_flush(cards, possible_cards, [flush_here, flush_suit])


def is_straight_flush(cards: list[Card], possible_cards: list[int], flush: list):
    """
    Проверка на наличии комбинации "Стрит Флеш" в заданном наборе карт
    :param cards: набор карт
    :param possible_cards: список возможных карт для заданной комбинации
    :param flush: данные о картах, из которых формируется флеш
    :return: list - сила комбинации, название и её карты
    """
    if flush[0]:
        straight_here, straight = is_straight_here(list(set(possible_cards)))

        if straight_here:
            return [8, 'straight Flush', straight, flush[1]]

    return is_four_of_the_kind(cards)


def is_four_of_the_kind(cards: list[Card]):
    """
    Проверка на наличии комбинации "Каре" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    four_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 4)
    if four_of_the_kind_here:
        return [7, 'Four of the Kind', uniq_card]

    return is_full_house(cards)


def is_full_house(cards: list[Card]):
    """
    Проверка на наличии комбинации "Фулл Хаус" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    three_of_the_kind_here, three_of_the_kind_uniq_card = is_some_of_a_kind_here(cards, 3)
    two_of_the_kind_here, two_of_the_kind_uniq_card = is_some_of_a_kind_here(cards, 2)

    if three_of_the_kind_here and two_of_the_kind_here:
        return [6, 'Full House', three_of_the_kind_uniq_card, two_of_the_kind_uniq_card]

    return is_flush(cards)


def is_flush(cards: list[Card]):
    """
    Проверка на наличии комбинации "Флеш" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    flush_here, flush_suit = is_flush_here(cards)

    if flush_here:
        return [5, 'Flush', sorted([card.value for card in cards if card.suit == flush_suit])[:-6:-1], flush_suit]

    return is_straight(cards)


def is_straight(cards: list[Card]):
    """
    Проверка на наличии комбинации "Стрит" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    straight_here, straight = is_straight_here(list(set([card.value for card in cards])))

    if straight_here:
        return [4, 'straight', straight]

    return is_three_of_a_kind(cards)


def is_three_of_a_kind(cards: list[Card]):
    """
    Проверка на наличии комбинации "Сет" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    three_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 3)

    if three_of_the_kind_here:
        return [3, 'Three of the Kind', uniq_card]

    return is_two_pair(cards)


def is_two_pair(cards: list[Card]):
    """
    Проверка на наличии комбинации "Две пары" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    two_of_the_kind_here, first_uniq_card = is_some_of_a_kind_here(cards, 2)
    two_of_the_kind_here, second_uniq_card = is_some_of_a_kind_here(cards, 2, first_uniq_card)

    if two_of_the_kind_here:
        return [2, 'Two Pair', first_uniq_card, second_uniq_card]

    return is_pair(cards)


def is_pair(cards: list[Card]):
    """
    Проверка на наличии комбинации "Пара" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    two_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 2)

    if two_of_the_kind_here:
        return [1, 'Pair', uniq_card]

    return is_kicker(cards)


def is_kicker(cards: list[Card]):
    """
    Проверка на наличии комбинации "Старшая карта" в заданном наборе карт
    :param cards: набор карт
    :return: list - сила комбинации, название и её карты
    """
    return [0, 'Kicker', sorted([card.value for card in cards])[-1]]
