import random

from agent import Agent
from board_utilities import BoardUtils


# upper limit of preferred ration of friendly soldiers to enemy soldiers
upper = 2
# lower limit of preferred ration of friendly soldiers to enemy soldiers
lower = 0.5

class RatioAgent(Agent):
    """
    builds on commiter agent.
    """

    def __init__(self):
        self.continent = None

    def get_new_continent(self, state):
        continent_scores = dict()
        for name, continent in state.board.continents.items():
            ratio = BoardUtils.get_continent_ratio(continent, state.player_to_move)
            if lower <= ratio <= upper:
                self.continent = continent
                return
            continent_scores[continent] = ratio
        min_val = float("inf")
        min_continents = []
        for continent in state.board.continents.values():
            val = min(abs(continent_scores[continent] - lower),
                      abs(continent_scores[continent] - upper))
            if val == min_val:
                min_continents.append(continent)
            if val < min_val:
                min_val = val
                min_continents = []
        if min_val == 0 or not min_continents:
            self.continent = random.choice(list(state.board.continents.values()))
            return
        self.continent = random.choice(min_continents)

    # overriding abstract method
    def reinforce_owned_territory(self, state):
        territories = set(state.board.border_territories(state.player_to_move))

        if not self.continent:
            self.get_new_continent(state)
        border_territories_in_continent = territories.intersection(self.continent.territories)
        if not border_territories_in_continent:
            self.get_new_continent(state)
            border_territories_in_continent = territories.intersection(
                self.continent.territories)
        if border_territories_in_continent:
            territory = border_territories_in_continent.pop()
            return territory
        return random.choice(list(territories))

    # overriding abstract method
    def reinforce_neutral_territory(self, state):
        territories = state.board.neutral_territories()
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        troop_count = 1
        if attacked_territory.troops > 1:
            troop_count = 2
        return troop_count

    # overriding abstract method
    def wants_to_attack(self, state):
        for territory in state.board.territories_to_attack_from(state.player_to_move):
            if territory.troops > 3:
                return True
        return False

    # overriding abstract method
    def select_attack_source(self, state):
        territories = list(state.board.territories_to_attack_from(state.player_to_move))
        for territory in territories:
            if territory.troops > 3:
                return territory
        else:
            return random.choice(territories)

    # overriding abstract method
    def select_attack_target(self, state, source):
        territories = source.enemy_neighbors()
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def select_attack_count(self, state, source):
        return source.troops - 1

    # overriding abstract method
    def wants_to_fortify(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        fortifiable_in_continent = set(territories).intersection(self.continent.territories)
        return bool(fortifiable_in_continent)

    # overriding abstract method
    def select_fortify_source(self, state, target):
        source = max([territory for territory in target.friendly_fortifiers()],
                     key=lambda territory: territory.troops)
        return source

    # overriding abstract method
    def select_fortify_target(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        fortifiable_in_continent = set(territories).intersection(self.continent.territories)
        target = random.choice(list(fortifiable_in_continent))
        return target

    # overriding abstract method
    def select_fortify_count(self, state, source):
        troop_count = source.troops - 1
        return troop_count
