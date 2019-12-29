class Continent:
    name = ''
    territories = []
    army_bonus = []

    def __init__(self, name, territories, army_bonus):
        self.name = name
        self.territories = territories
        self.army_bonus = army_bonus

    def add_territory(self, territory):
        self.territories.append(territory)

    def __str__(self):
        return f'{self.name} with an army bonus of {self.army_bonus} and territories:\n' + str(self.territories) + '\n'

    def get_ruler(self):
        rulers = set()
        for territory in self.territories:
            rulers.add(territory.ruler)

        if len(rulers) == 1:
            return rulers.pop()
        else:
            return None
