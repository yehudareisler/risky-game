from enum import Enum


class Card:
    card_type = None
    territory_name = ''

    def __init__(self, card_type, territory_name):
        self.card_type = card_type
        self.territory_name = territory_name


class CardType(Enum):
    WILDCARD = 0
    INFANTRY = 1
    CAVALRY = 2
    ARTILLERY = 3