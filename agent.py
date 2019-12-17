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

    # return: boolean, whether the agent wants to fortify or not
    # abstract method
    def wants_to_fortify(self, state):
        pass
