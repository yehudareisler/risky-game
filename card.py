from enum import Enum


class Card:
    card_type = None
    territory_name = ''

    def __init__(self, territory_name, card_type):
        self.territory_name = territory_name
        self.card_type = card_type

    def __str__(self):
        return f'Card of {self.territory_name} with {self.card_type} type'


class CardType(Enum):
    WILDCARD = 0
    INFANTRY = 1
    CAVALRY = 2
    ARTILLERY = 3

    def __str__(self):
        return self.name
