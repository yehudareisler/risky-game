from game import Game
from card import CardType
from exceptions import *
from logger import Logger


class Player:

    def __init__(self, name, agent):
        self.name = name
        self.agent = agent
        self.available_troops = 0
        self.card_count = {
            CardType.WILDCARD: 0,
            CardType.INFANTRY: 0,
            CardType.CAVALRY: 0,
            CardType.ARTILLERY: 0
        }

    def __str__(self):
        return self.name

    # To simplify the implementation, all players must turn in a set as soon as they can.
    # Additionally, this rule:
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # If any of the 3 cards you trade in shows the picture of a territory you occupy, you receive 2 extra armies.)
    # You must place both those armies onto that particular territory.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # is no longer applied.
    # To be implemented if more complexity is wanted.
    def trades_in_cards(self, state):
        total_count = self.card_count[CardType.WILDCARD] + \
                      self.card_count[CardType.INFANTRY] + \
                      self.card_count[CardType.CAVALRY] + \
                      self.card_count[CardType.ARTILLERY]
        if total_count > 2:

            # wildcard combination
            if self.card_count[CardType.WILDCARD] > 0:
                if self.card_count[CardType.INFANTRY] > 0:
                    if self.card_count[CardType.CAVALRY] > 0:
                        self.card_count[CardType.WILDCARD] -= 1
                        self.card_count[CardType.INFANTRY] -= 1
                        self.card_count[CardType.CAVALRY] -= 1
                        Logger.log(f'{self.name} trades in a wildcard combination', state.verbose)
                        return True

                    elif self.card_count[CardType.ARTILLERY] > 0:
                        self.card_count[CardType.WILDCARD] -= 1
                        self.card_count[CardType.INFANTRY] -= 1
                        self.card_count[CardType.ARTILLERY] -= 1
                        Logger.log(f'{self.name} trades in a wildcard combination', state.verbose)
                        return True

                elif self.card_count[CardType.CAVALRY] > 0 and self.card_count[CardType.ARTILLERY] > 0:
                    self.card_count[CardType.WILDCARD] -= 1
                    self.card_count[CardType.CAVALRY] -= 1
                    self.card_count[CardType.ARTILLERY] -= 1
                    Logger.log(f'{self.name} trades in a wildcard combination', state.verbose)
                    return True

            # three of a kind
            if self.card_count[CardType.INFANTRY] > 2:
                self.card_count[CardType.INFANTRY] -= 3
                Logger.log(f'{self.name} trades in three infantry cards', state.verbose)
                return True

            if self.card_count[CardType.CAVALRY] > 2:
                self.card_count[CardType.CAVALRY] -= 3
                Logger.log(f'{self.name} trades in three cavalry cards', state.verbose)
                return True

            if self.card_count[CardType.ARTILLERY] > 2:
                self.card_count[CardType.ARTILLERY] -= 3
                Logger.log(f'{self.name} trades in three artillery cards', state.verbose)
                return True

            # one of each
            if self.card_count[CardType.INFANTRY] > 0 \
                    and self.card_count[CardType.CAVALRY] > 0 \
                    and self.card_count[CardType.ARTILLERY] > 0:
                self.card_count[CardType.INFANTRY] -= 1
                self.card_count[CardType.CAVALRY] -= 1
                self.card_count[CardType.ARTILLERY] -= 1
                Logger.log(f'{self.name} trades in one card of each type', state.verbose)
                return True

            # no card combination
            return False

        else:
            return False

    def reinforce_owned_territory(self, state):
        territory = self.agent.reinforce_owned_territory(state)
        if territory.ruler != self:
            Logger.log(f'{self} is not the ruler of {territory}!', state.verbose)
            raise TerritoryNotOwnedByPlayerException()
        else:
            Logger.log(f'{self} reinforces {territory}', state.verbose)
            territory.troops += 1

    def reinforce_neutral_territory(self, state):
        territory = self.agent.reinforce_neutral_territory(state)
        if territory.ruler:
            Logger.log(f'{territory} is not a neutral territory!', state.verbose)
            raise TerritoryNotNeutralException()
        else:
            Logger.log(f'Neutral {territory} reinforced by {self}', state.verbose)
            territory.troops += 1

    def fortify(self, state):
        # decide target territory
        target = self.agent.select_fortify_target(state)
        # decide source territory
        source = self.agent.select_fortify_source(state, target)
        if target.ruler != self:
            Logger.log(f'Cannot fortify enemy {target}!', state.verbose)
            raise CannotFortifyTerritoryException()
        else:
            # decide fortify count
            fortify_count = self.agent.select_fortify_count(state, source)
            Logger.log(f'{self} fortifies {target} from {source} with {fortify_count} troops', state.verbose)
            target.troops += fortify_count
            source.troops -= fortify_count

    # return the number of troops (1 or 2) committed to defend against an attack
    def defend_territory(self, state, attacked_territory):
        troops_to_commit = self.agent.defend_territory(state, attacked_territory)
        return troops_to_commit

    # solves a battle situation
    def attack_territory(self, state, source_territory, target_territory, attacker_count):
        attacker_dice_rolls = sorted([Game.dice_roll() for _ in range(attacker_count)], reverse=True)

        if target_territory.is_neutral():
            defender_count = state.player_to_wait.defend_territory(state, target_territory)
            Logger.log(f'Neutrals defend with {defender_count} troops', state.verbose)
        else:
            defender_count = target_territory.ruler.defend_territory(state, target_territory)
            Logger.log(f'{target_territory.ruler} defends with {defender_count} troops', state.verbose)
        defender_dice_rolls = sorted([Game.dice_roll() for _ in range(defender_count)], reverse=True)

        if defender_dice_rolls[0] >= attacker_dice_rolls[0]:
            source_territory.troops -= 1
        else:
            target_territory.troops -= 1

        # continue dice roll comparison in case both players committed at least 2 troops
        if defender_count > 1 and attacker_count > 1:
            if defender_dice_rolls[1] >= attacker_dice_rolls[1]:
                source_territory.troops -= 1
            else:
                target_territory.troops -= 1

        # transfer ownership if the attacked territory loses all of its troops
        if target_territory.troops == 0:
            Logger.log(f'{target_territory} has been conquered by {self}', state.verbose)
            target_territory.ruler = self
            target_territory.troops = attacker_count
            target_territory.fill_color = source_territory.fill_color
            state.attack_successful = True

    def receive_troops(self, state):
        # calculate occupied territory bonus
        occupied_territories = state.board.occupied_territories(self)
        territory_bonus = max(len(occupied_territories), 9)//3

        # calculate occupied continent bonus
        occupied_continents = state.board.occupied_continents(self)
        continent_bonus = 0
        for continent in occupied_continents:
            continent_bonus += continent.army_bonus

        # calculate card bonus
        card_bonus = 0
        if self.trades_in_cards(state):
            card_bonus += state.get_card_bonus()

        self.available_troops = territory_bonus + continent_bonus + card_bonus
        Logger.log(f'{self.name} receives {self.available_troops} troops ( '
                   f'{territory_bonus}/{continent_bonus}/{card_bonus})', state.verbose)

    def place_new_troops(self, state):
        for _ in range(self.available_troops):
            self.reinforce_owned_territory(state)

        self.available_troops = 0

    def attack(self, state):
        state.attack_successful = False
        # decide source territory
        source = self.agent.select_attack_source(state)
        # decide target territory
        target = self.agent.select_attack_target(state, source)
        if target.ruler == self:
            Logger.log(f'Cannot attack friendly {target}!', state.verbose)
            raise CannotAttackTerritoryException()
        else:
            # decide attacker count
            attacker_count = self.agent.select_attack_count(state, source)
            Logger.log(f'{self} attacks {target} from {source} with {attacker_count} troops', state.verbose)
            self.attack_territory(state, source, target, attacker_count)

    # decide whether we want to attack this turn or not
    def wants_to_attack(self, state):
        return self.agent.wants_to_attack(state)

    # decide whether we want to fortify this turn or not
    def wants_to_fortify(self, state):
        return self.agent.wants_to_fortify(state)

    def take_turn(self, state):
        self.receive_troops(state)
        self.place_new_troops(state)

        # check if player can attack
        source_territories = state.board.territories_to_attack_from(self)
        while source_territories and self.wants_to_attack(state):
            self.attack(state)
            source_territories = state.board.territories_to_attack_from(self)
        Logger.log(f'{self} stopped attacking', state.verbose)

        if state.attack_successful and state.pile.cards:
            card = state.pile.draw_card()
            self.card_count[card.card_type] += 1

        # check if player can fortify
        target_territories = state.board.territories_to_fortify_to(self)
        if target_territories and self.wants_to_fortify(state):
            self.fortify(state)
