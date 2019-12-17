class Territory:
    name = ''
    neighbors = []
    ruler = ''
    troops = 0

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_neutral(self):
        return not self.ruler
