class Goals:

    def __init__(self, name, country_list, goal_value):
        self.name = name
        self.value = goal_value
        self.terortorys = country_list

    def countrys_needed_for_goal(self, state, player):
        i = 0
        terortorys_for_goal = []
        for terortory in self.terortorys:
            if terortory.ruler == player:
                terortorys_for_goal[i] = terortory
                i = i + 1
        return terortorys_for_goal
