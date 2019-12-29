class Path:

    def __init__(self, from_territory, to_territory):
        self.from_territory = from_territory
        self.to_territory = to_territory

    def __repr__(self):
        return f'Path from {self.from_territory} to {self.to_territory}'
