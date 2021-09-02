import random

from agent import Agent


class PlanCommitter(Agent):
    """
    an agent that attacks when it has more than three soldiers in a territory, then moves all
    soldiers in. It reinforces a specific continent it is trying to conquer. It prefers to attack
    countries in the continent.
    """

    def __init__(self):
        self.continent = None
        self.reinforce_territory = None

    def get_new_continent(self, state):
        self.continent = random.choice([v for k, v in state.board.continents.items()])

    # overriding abstract method
    def reinforce_owned_territory(self, state):
        territories = set(state.board.border_territories(state.player_to_move))
        if self.reinforce_territory in territories:
            territory = self.reinforce_territory
            if state.player_to_move.available_troops <= 1:
                self.reinforce_territory = None
            return territory
        territories = set(state.board.border_territories(state.player_to_move))
        if not self.continent:
            self.get_new_continent(state)
        while True:
            border_territories_in_continent = territories.intersection(self.continent.territories)
            if not border_territories_in_continent:
                self.get_new_continent(state)
            else:
                territory = random.choice(list(border_territories_in_continent))
                self.reinforce_territory = territory
                return territory

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
        possible_sources = [territory for territory in territories if territory.troops>3]
        if possible_sources:
            return random.choice(possible_sources)
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
        return random.random() < 0.9

    # overriding abstract method
    def select_fortify_source(self, state, target):
        source = max([territory for territory in target.friendly_fortifiers()],
                     key=lambda territory: territory.troops)
        return source

    # overriding abstract method
    def select_fortify_target(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        while True:
            fortifiable_in_continent = set(territories).intersection(self.continent.territories)
            if not fortifiable_in_continent:
                self.get_new_continent(state)
                continue
            target = random.choice(list(fortifiable_in_continent))
            return target

    # overriding abstract method
    def select_fortify_count(self, state, source):
        troop_count = source.troops - 1
        return troop_count
