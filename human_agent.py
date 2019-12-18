from agent import Agent


class HumanAgent(Agent):
    # overriding abstract method
    def reinforce_owned_territory(self, state):
        territory_name = input('Reinforce territory: ')
        return state.board.territories[territory_name]

    # overriding abstract method
    def reinforce_neutral_territory(self, state):
        territory_name = input('Reinforce territory: ')
        return state.board.territories[territory_name]

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        troop_count = int(input('Troops to commit to defend ' + attacked_territory + ': '))
        return troop_count

    # overriding abstract method
    def wants_to_attack(self, state):
        wants_to_attack = input('Attack this turn (Y-Yes, other-No): ')
        if wants_to_attack == 'Y':
            return True
        else:
            return False

    # overriding abstract method
    def wants_to_fortify(self, state):
        wants_to_fortify = input('Fortify this turn (Y-Yes, other-No): ')
        if wants_to_fortify == 'Y':
            return True
        else:
            return False

    # overriding abstract method
    def fortify_territory(self, state):
        to_territory_name = input('Fortify territory: ')
        from_territory_name = input('From neighboring territory: ')
        troop_count = int(input('Move this many troops: '))
        return to_territory_name, from_territory_name, troop_count