from game import Game
from card import CardType
from exceptions import *


class Player:
    available_troops = 0
    cards = []
    agent = None
    name = ''

    def __init__(self, name, agent):
        self.name = name
        self.agent = agent
        self.available_troops = 0
        self.cards = []

    def __repr__(self):
        return self.name

    # To simplify the implementation, all players must turn in a set as soon as they can.
    # Additionally, this rule:
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # If any of the 3 cards you trade in shows the picture of a territory you occupy, you receive 2 extra armies.)
    # You must place both those armies onto that particular territory.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # is no longer applied.
    # To be implemented if more complexity is wanted.
    def trades_in_cards(self):
        if len(self.cards) > 2:
            wildcard_count = sum(card.card_type == CardType.WILDCARD for card in self.cards)
            infantry_count = sum(card.card_type == CardType.INFANTRY for card in self.cards)
            cavalry_count = sum(card.card_type == CardType.CAVALRY for card in self.cards)
            artillery_count = sum(card.card_type == CardType.ARTILLERY for card in self.cards)

            # wildcard combination
            if wildcard_count > 0:
                if infantry_count > 0:
                    if cavalry_count > 0:
                        wildcard_count -= 1
                        infantry_count -= 1
                        cavalry_count -= 1
                        return True

                    elif artillery_count > 0:
                        wildcard_count -= 1
                        infantry_count -= 1
                        artillery_count -= 1
                        return True

                elif cavalry_count > 0 and artillery_count > 0:
                    wildcard_count -= 1
                    cavalry_count -= 1
                    artillery_count -= 1
                    return True

            # three of a kind
            if infantry_count > 2:
                infantry_count -= 3
                return True

            if cavalry_count > 2:
                cavalry_count -= 3
                return True

            if artillery_count > 2:
                artillery_count -= 3
                return True

            # one of each
            if infantry_count > 0 and cavalry_count > 0 and artillery_count > 0:
                infantry_count -= 1
                cavalry_count -= 1
                artillery_count -= 1
                return True

            # no card combination
            return False

        else:
            return False

    def reinforce_owned_territory(self, state):
        territory = self.agent.reinforce_owned_territory(state)
        if territory.ruler != self.name:
            raise TerritoryNotOwnedByPlayerException()
        else:
            territory.troops += 1

    def reinforce_neutral_territory(self, state):
        name_of_territory_to_reinforce = self.agent.reinforce_neutral_territory(state)
        territory = state.board.territories[name_of_territory_to_reinforce]
        if territory.ruler != '':
            raise TerritoryNotNeutralException()
        else:
            territory.troops += 1

    def fortify_territory(self, state):
        name_of_territory_to_fortify, name_of_neighbor, troop_count = self.agent.fortify_territory(state)
        territory = state.board.territories[name_of_territory_to_fortify]
        neighbor = state.board.territories[name_of_neighbor]
        territory.troops += troop_count
        neighbor += troop_count

    # return the number of troops (1 or 2) committed to defend against an attack
    def defend_territory(self, state, attacked_territory):
        troops_to_commit = self.agent.defend_territory(state, attacked_territory)
        return troops_to_commit

    # solves a battle situation
    def attack_territory(self, state, source_territory, target_territory, attacker_count):
        attacker_dice_rolls = sorted([Game.dice_roll() for _ in range(attacker_count)], reverse=True)

        defender_count = target_territory.ruler.defend_territory(state, target_territory)
        defender_dice_rolls = sorted([Game.dice_roll() for _ in range(defender_count)], reverse=True)

        if defender_dice_rolls[0] >= attacker_dice_rolls[0]:
            source_territory.troops -= 1
            attacker_count -= 1
        else:
            target_territory.troops -= 1

        # continue dice roll comparison in case both players committed at least 2 troops
        if defender_count > 1 and attacker_count > 1:
            if defender_dice_rolls[1] >= attacker_dice_rolls[1]:
                source_territory.troops -= 1
                attacker_count -= 1
            else:
                target_territory.troops -= 1

        # transfer ownership if the attacked territory loses all of its troops
        if target_territory.troops == 0:
            target_territory.ruler = self
            target_territory.troops = attacker_count

    def receive_troops(self, state):
        # calculate occupied territory bonus
        occupied_territories = state.board.territories_occupied_by(self)
        territory_bonus = max(len(occupied_territories), 9)//3

        # calculate occupied continent bonus
        occupied_continents = state.board.continents_occupied_by(self)
        continent_bonus = 0
        for continent in occupied_continents:
            continent_bonus += continent.army_bonus

        # calculate card bonus
        card_bonus = 0
        if self.trades_in_cards():
            card_bonus += state.get_card_bonus(state)

        self.available_troops = territory_bonus + continent_bonus + card_bonus

    def place_new_troops(self, state):
        for _ in range(self.available_troops):
            self.reinforce_owned_territory(state)

        self.available_troops = 0

    def attack(self, state):
        pass

    def territories_to_attack(self, state):
        target_territories = set()
        occupied_territories = state.board.occupied_territories(state)
        for territory in occupied_territories:
            for neighbor in territory.neighbors:
                if neighbor.ruler != self:
                    target_territories.add(neighbor)

        return target_territories

    def territories_on_the_border(self, state):
        border_territories = set()
        occupied_territories = state.board.occupied_territories(self)
        for territory in occupied_territories:
            for neighbor in territory.neighbors:
                if neighbor.ruler != self:
                    border_territories.add(territory)
                    break

        return border_territories

    # decide whether we want to attack this turn or not
    def wants_to_attack(self, state):
        return self.agent.wants_to_attack(self, state)

    # decide whether we want to fortify this turn or not
    def wants_to_fortify(self, state):
        return self.agent.wants_to_fortify(self, state)

    def take_turn(self, state):
        self.receive_troops(state)
        self.place_new_troops(state)
        if self.wants_to_attack(state):
            self.attack(state)
        if self.wants_to_fortify(state):
            self.fortify_territory(state)
