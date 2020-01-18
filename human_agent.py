from agent import Agent


class HumanAgent(Agent):
    # overriding abstract method
    def reinforce_owned_territory(self, state):
        territory_name = input('Reinforce owned territory: ').strip()
        return state.board.territories[territory_name]

    # overriding abstract method
    def reinforce_neutral_territory(self, state):
        territory_name = input('Reinforce neutral territory: ').strip()
        return state.board.territories[territory_name]

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        troop_count = int(input('Troops committed to defend ' + attacked_territory + ': '))
        return troop_count

    # overriding abstract method
    def wants_to_attack(self, state):
        wants_to_attack = input('Attack this turn (Y-Yes, other-No): ').strip()
        if wants_to_attack == 'Y':
            return True
        else:
            return False

    # overriding abstract method
    def select_attack_source(self, state):
        territory_name = input('Attack an enemy territory from: ').strip()
        return state.board.territories[territory_name]

    # overriding abstract method
    def select_attack_target(self, state, source):
        territory_name = input('Attack enemy territory: ').strip()
        return state.board.territories[territory_name]

    # overriding abstract method
    def select_attack_count(self, state, source):
        troop_count = int(input('Troops committed to attack: '))
        return troop_count

    # overriding abstract method
    def wants_to_fortify(self, state):
        wants_to_fortify = input('Fortify this turn (Y-Yes, other-No): ').strip()
        if wants_to_fortify == 'Y':
            return True
        else:
            return False

    # overriding abstract method
    def select_fortify_source(self, state, target):
        from_territory_name = input(f'Fortify {target} from territory: ').strip()
        return state.board.territories[from_territory_name]

    # overriding abstract method
    def select_fortify_target(self, state):
        to_territory_name = input('Fortify target territory: ').strip()
        return state.board.territories[to_territory_name]

    # overriding abstract method
    def select_fortify_count(self, state, source):
        troop_count = int(input('Move this many troops: '))
        return troop_count
