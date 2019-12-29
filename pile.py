import random

from card import Card, CardType


class Pile:

    def __init__(self, cards):
        self.cards = cards

    def __getitem__(self, key):
        return self.cards[key]

    def __str__(self):
        representation = f'Pile with {len(self.cards)} cards:\n'
        for card in self.cards:
            representation += f'{card}\n'

        return representation

    @staticmethod
    def from_config_file(path_to_file):
        new_cards = [
            Card(None, CardType.WILDCARD),
            Card(None, CardType.WILDCARD)
        ]

        with open(path_to_file) as f:
            card_count = int(f.readline().strip())
            for _ in range(card_count):
                territory = f.readline().strip()
                card_type = f.readline().strip()
                new_cards.append(Card(territory, CardType[card_type]))
        return Pile(new_cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def remove_card(self, card):
        self.cards.remove(card)

    def remove_card_with_index(self, index):
        self.cards.remove(self.cards[index])

    def add_card(self, card):
        self.cards.append(card)

    def draw_card(self):
        return self.cards.pop(0)
