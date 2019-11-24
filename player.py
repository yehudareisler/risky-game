from game import Game
from card import CardType


class Player:
    available_troops = 0
    cards = []
    agent = None

    def __init__(self):
        self.available_troops = 0
        self.cards = []

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

    def claim_territory(self, game_state):
        return self.agent.claim_territory(game_state)

    def reinforce_territory(self, game_state):
        return self.agent.reinforce_territory(game_state)

    def fortify_territory(self, game_state):
        return self.agent.fortify_territory(game_state)

    # return the number of troops (1 or 2) committed to defend against an attack
    def defend_territory(self, game_state, attacked_territory):
        return self.agent.defend_territory(game_state, attacked_territory)

    # solves a battle situation
    def attack_territory(self, game_state, source_territory, target_territory, attacker_count):
        attacker_dice_rolls = sorted([Game.dice_roll() for _ in range(attacker_count)], reverse=True)

        defender_count = target_territory.ruler.defend_territory(game_state, target_territory)
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

    def get_occupied_territories(self, game_state):
        occupied_territories = []
        for territory in game_state.game_board.territories:
            if territory.ruler == self:
                occupied_territories.append(territory)

        return occupied_territories

    def get_occupied_continents(self, game_state):
        occupied_continents = []
        for continent in game_state.game_board.continents:
            continent_ruler = continent.get_ruler()
            if continent_ruler == self:
                occupied_continents.append(continent)

        return occupied_continents

    def receive_troops(self, game_state):
        # calculate occupied territory bonus
        occupied_territories = self.get_occupied_territories(game_state)
        territory_bonus = max(len(occupied_territories), 9)//3

        # calculate occupied continent bonus
        occupied_continents = self.get_occupied_continents(game_state)
        continent_bonus = 0
        for continent in occupied_continents:
            continent_bonus += continent.army_bonus

        # calculate card bonus
        card_bonus = 0
        if self.trades_in_cards():
            card_bonus += game_state.get_card_bonus(game_state)

        self.available_troops = territory_bonus + continent_bonus + card_bonus

    def place_new_troops(self, game_state):
        for _ in range(self.available_troops):
            self.reinforce_territory(game_state)

        self.available_troops = 0

    def attack(self, game_state):
        pass

    def get_territories_to_attack(self, game_state):
        target_territories = set()
        occupied_territories = self.get_occupied_territories(game_state)
        for territory in occupied_territories:
            for neighbor in territory.neighbors:
                if neighbor.ruler != self:
                    target_territories.add(neighbor)

        return target_territories

    def territories_on_the_border(self, game_state):
        border_territories = set()
        occupied_territories = self.get_occupied_territories(game_state)
        for territory in occupied_territories:
            for neighbor in territory.neighbors:
                if neighbor.ruler != self:
                    border_territories.add(territory)
                    break

        return border_territories

    # decide whether we want to attack this turn or not
    def wants_to_attack(self, game_state):
        pass

    # decide whether we want to fortify this turn or not
    def wants_to_fortify(self, game_state):
        pass

    def take_turn(self, game_state):
        self.receive_troops(game_state)
        self.place_new_troops(game_state)
        if self.wants_to_attack(game_state):
            self.attack(game_state)
        if self.wants_to_fortify(game_state):
            self.fortify_territory(game_state)
