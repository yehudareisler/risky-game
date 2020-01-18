class TerritoryNotOwnedByPlayerException(Exception):
    pass


class TerritoryNotNeutralException(Exception):
    pass


class CannotAttackTerritoryException(Exception):
    pass

class CannotFortifyTerritoryException(Exception):
    pass