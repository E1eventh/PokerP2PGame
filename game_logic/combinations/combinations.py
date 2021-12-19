from game_logic.card.card import Card


def get_strongest_combination(cards: list[Card]):
    return is_royal_flush(sorted(cards))


def is_flush_here(flush_cards: list[Card]):
    suits = [card.suit for card in flush_cards]
    uniq_suits = list(set(suits))

    if len(uniq_suits) == 1:
        return True, uniq_suits[0]
    else:
        for uniq_suit in uniq_suits:
            if suits.count(uniq_suit) >= 5:
                return True, uniq_suit

    return False, ''


def is_straith_here(straith_cards: list[int]):
    smallest_straith = False
    straith_here = False
    straith = (0, 0)

    if len(straith_cards) < 5:
        return straith_here, straith

    if len(straith_cards) == 7:
        if straith_cards[6] - straith_cards[2] == 4:
            straith_here = True
            straith = (straith_cards[2], straith_cards[6])
        elif straith_cards[6] - straith_cards[3] == 9:
            smallest_straith = True
        straith_cards = straith_cards[:6]

    if len(straith_cards) == 6 and not straith_here:
        if straith_cards[5] - straith_cards[1] == 4:
            straith_here = True
            straith = (straith_cards[1], straith_cards[5])
        elif straith_cards[5] - straith_cards[3] == 9:
            smallest_straith = True
        straith_cards = straith_cards[:5]

    if straith_cards[4] - straith_cards[0] == 4 and not straith_here:
        straith_here = True
        straith = (straith_cards[0], straith_cards[4])
    elif straith_cards[4] - straith_cards[3] == 9:
        smallest_straith = True

    if not straith_here and smallest_straith:
        straith_here = True
        straith = (14, 5)

    return straith_here, straith


def is_some_of_a_kind_here(cards: list[Card], counter, excluded_card=None):
    cards_values = [card.value for card in cards if card.value != excluded_card]

    uniq_card_values = sorted(list(set(cards_values)))
    uniq_card_values.reverse()

    for uniq_card in uniq_card_values:
        if cards_values.count(uniq_card) == counter:
            return True, uniq_card

    return False, 0


def is_royal_flush(cards: list[Card]):
    flush_here, flush_suit = is_flush_here(cards)
    possible_cards = [card.value for card in cards if card.suit == flush_suit]

    if flush_here:
        if sorted(possible_cards)[:-6:-1] == list(range(14, 9, -1)):
            return [9, 'Royal Flush', flush_suit]

    return is_straight_flush(cards, possible_cards, [flush_here, flush_suit])


def is_straight_flush(cards: list[Card], possible_cards: list[int], flush: list):
    if flush[0]:
        straith_here, straith = is_straith_here(list(set(possible_cards)))

        if straith_here:
            return [8, 'Straith Flush', straith, flush[1]]

    return is_four_of_the_kind(cards)


def is_four_of_the_kind(cards: list[Card]):
    four_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 4)
    if four_of_the_kind_here:
        return [7, 'Four of the Kind', uniq_card]

    return is_full_house(cards)


def is_full_house(cards: list[Card]):
    three_of_the_kind_here, three_of_the_kind_uniq_card = is_some_of_a_kind_here(cards, 3)
    two_of_the_kind_here, two_of_the_kind_uniq_card = is_some_of_a_kind_here(cards, 2)

    if three_of_the_kind_here and two_of_the_kind_here:
        return [6, 'Full House', three_of_the_kind_uniq_card, two_of_the_kind_uniq_card]

    return is_flush(cards)


def is_flush(cards: list[Card]):
    flush_here, flush_suit = is_flush_here(cards)

    if flush_here:
        return [5, 'Flush', sorted([card.value for card in cards if card.suit == flush_suit])[:-6:-1], flush_suit]

    return is_straight(cards)


def is_straight(cards: list[Card]):
    straith_here, straith = is_straith_here(list(set([card.value for card in cards])))

    if straith_here:
        return [4, 'Straith', straith]

    return is_three_of_a_kind(cards)


def is_three_of_a_kind(cards: list[Card]):
    three_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 3)

    if three_of_the_kind_here:
        return [3, 'Three of the Kind', uniq_card]

    return is_two_pair(cards)


def is_two_pair(cards: list[Card]):
    two_of_the_kind_here, first_uniq_card = is_some_of_a_kind_here(cards, 2)
    two_of_the_kind_here, second_uniq_card = is_some_of_a_kind_here(cards, 2, first_uniq_card)

    if two_of_the_kind_here:
        return [2, 'Two Pair', first_uniq_card, second_uniq_card]

    return is_pair(cards)


def is_pair(cards: list[Card]):
    two_of_the_kind_here, uniq_card = is_some_of_a_kind_here(cards, 2)

    if two_of_the_kind_here:
        return [1, 'Pair', uniq_card]

    return is_kicker(cards)


def is_kicker(cards: list[Card]):
    return [0, 'Kicker', sorted([card.value for card in cards])[-1]]


if __name__ == '__main__':
    cards = [Card(2, 'H'), Card(3, 'H'), Card(4, 'H'), Card(5, 'H'), Card(13, 'H'), Card(14, 'H'), Card(9, 'H')]

    print(get_strongest_combination(cards))
