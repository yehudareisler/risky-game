from abc import ABC, abstractmethod


class Agent(ABC):
    # return: name of the territory to be reinforced
    # abstract method
    def reinforce_territory(self, state):
        pass

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
        pass

    # return: boolean, whether the agent wants to attack or not
    # abstract method
    def wants_to_attack(self, state):
        pass

    # return: territory, attack source
    # abstract method
    def select_attack_source(self, state):
        pass

    # return: territory, attack target
    # abstract method
    def select_attack_target(self, state, source):
        pass

    # return: integer, troops involved in attack
    # abstract method
    def select_attack_count(self, state, source):
        pass

    # return: boolean, whether the agent wants to fortify or not
    # abstract method
    def wants_to_fortify(self, state):
        pass

    # return: territory, fortify source
    # abstract method
    def select_fortify_source(self, state, target):
        pass

    # return: territory, fortify target
    # abstract method
    def select_fortify_target(self, state):
        pass

    # return: integer, troops involved in fortification
    # abstract method
    def select_fortify_count(self, state, source):
        pass
