import random

from card import Card, CardType


class Pile:
    cards = []

    def __init__(self):
        self.cards = []

    def initialize_game_card_pile_from_config_file(self, path_to_file):
        self.cards.append(Card(CardType.WILDCARD, None))
        self.cards.append(Card(CardType.WILDCARD, None))

        with open(path_to_file) as f:
            territory = f.readline()
            card_type = f.readline()
            self.cards.append(Card(territory, CardType[card_type]))

    def shuffle(self):
        random.shuffle(self.cards)

    def remove_card(self, card):
        self.cards.remove(card)

    def add_card(self, card):
        self.cards.append(card)
