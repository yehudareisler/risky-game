class Continent:
    name = ''
    terriories = []
    armyBonus = []

    def __init__(self, name, territories, armyBonus):
        self.territories = territories
        self.armyBonus = armyBonus

    def addTeritory(self, territory):
        self.territories.append(territory)
