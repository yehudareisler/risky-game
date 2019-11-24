class Agent:
    # decide:
    # which is the best territory to claim next in the setup phase
    def claim_territory(self, game_state):
        pass

    # decide:
    # where to add the next available troop
    def reinforce_territory(self, game_state):
        pass

    # decide:
    # which territory to fortify
    # from which neighboring territory
    # with how many troops
    def fortify_territory(self, game_state):
        pass

    # decide:
    # the number of troops (1 or 2) committed to defend against an attack on a particular territory
    def defend_territory(self, game_state, attacked_territory):
        pass
