class Territory:
    name = ''
    neighbors = []

    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __repr__(self):
        return self.name
