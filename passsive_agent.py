from abc import ABC, abstractmethod
import random


class Agent(ABC):
    # return: name of the territory to be reinforced
    # abstract method
    def reinforce_territory(self, state):
        territories = state.board.border_territories(state.player_to_move)
        territory = random.choice(territories)
        return territory

    # return: <to>, <from>, <troop_count>
    # <to> which territory to fortify
    # <from> which neighboring territory
    # <troop_count> with how many troops
    # abstract method
    def fortify_territory(self, state):
        pass

    # return: 1 or 2 (number of troops committed to defend attacked_territory)
    # abstract method
    def defend_territory(self, state, attacked_territory):
        return 2

    # return: boolean, whether the agent wants to attack or not
    # abstract method
    def wants_to_attack(self, state):
        return random.random() < 0.5

    # return: territory, attack source
    # abstract method
    def select_attack_source(self, state):
        territories = list(state.board.territories_to_attack_from(state.player_to_move))
        territory = random.choice(territories)
        return territory

    # return: territory, attack target
    # abstract method
    def select_attack_target(self, state, source):
        territories = list(source.enemy_neighbors())
        territory = random.choice(territories)
        return territory

    # return: integer, troops involved in attack
    # abstract method
    def select_attack_count(self, state, source):
        return source.troops

    # return: boolean, whether the agent wants to fortify or not
    # abstract method
    def wants_to_fortify(self, state):
        return random.random() < 0.8

    # return: territory, fortify source
    # abstract method
    def select_fortify_source(self, state, target):
        source = random.choice(target.friendly_fortifiers())
        return source

    # return: territory, fortify target
    # abstract method
    def select_fortify_target(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        target = random.choice(territories)
        return target

    # return: integer, troops involved in fortification
    # abstract method
    def select_fortify_count(self, state, source):
        return source.troops / 2
