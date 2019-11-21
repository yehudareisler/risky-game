from game import Game
from gamemap import GameMap

my_game_map = GameMap({}, [])
my_game_map.initialize_from_config_file('game-map.cfg')
print(my_game_map)
