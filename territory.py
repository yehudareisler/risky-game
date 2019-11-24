class Territory:
    name = ''
    neighbors = []
    ruler = None
    troops = 0

    def __init__(self, name):
        self.name = name

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __repr__(self):
        return self.name
