import copy


attacking_ratio = 0.86
b_player_name = "attack_above_three"
# PLAYER_1 = "Bot_1"
# PLAYER_2 = "Bot_2"
import territory


def get_continent_ratio(continent, player_a):
    player_a_troops = 0
    player_b_troops = 0
    for land in continent.territories:
        if land.ruler == player_a:
            player_a_troops += land.troops
        else:
            player_b_troops += land.troops

    return player_a_troops / player_b_troops


def find_territory_ratio(territory_a, territory_b):
    return territory_a.troops / territory_b.troops


# assuming neighbors
def cmp_ter_by_troops(territory_a, territory_b):
    return territory_a.troops - territory_b.troops


def get_neighbor_sorted_by_rat(base_territory):
    sorted_neighbors = []

    # attacking only from border ter
    for neighbor in base_territory.neighbors:
        if neighbor.ruler != base_territory.ruler:
            sorted_neighbors.append(neighbor)

    sorted_neighbors = sorted(sorted_neighbors, key=territory.get_troops)
    return sorted_neighbors


#
def calculate_path_value(path, state, player):
    # length = len(path)
    index = 1
    if player.name == b_player_name:
        index = -1

    copied_state = copy.deepcopy(state)
    player_a_init = copied_state.players[0].calculate_troops_addition(state)
    player_b_init = copied_state.players[1].calculate_troops_addition(state)
    for land in path:
        # copied_state.board.territories[land].ruler = player
        land.ruler = player
    player_a = copied_state.players[0].calculate_troops_addition(state)
    player_b = copied_state.players[1].calculate_troops_addition(state)

    player_a -= player_a_init
    player_b -= player_b_init

    return (player_a - player_b) * index


# find the best continent and in which take the infimum
def choose_soldier_addition(player, continent):
    pass


# place soldiers and attakc where you can
def handel_turn(player):
    pass


# find continent with biggest ratio
def choose_continent_to_attak():
    pass


def path_weight(path, state):
    sum = 0
    for area in path:
        try:
            sum += state.board.territories[area.name].troops
        except:
            sum += state.board.territories[area].troops
    return sum


def board_to_graph_attacking_graph(board, player):
    graph = {}
    for land in board.border_territories(player):
        graph[land] = []
        for neighbor in board.territories[land.name].neighbors:
            # if not (land.ruler == player.name == neighbor.ruler) and find_territory_ratio(land, neighbor) > attacking_ratio:
            graph[land].append(neighbor.name)
    return graph


def printAllPathsUtil(state, graph, u, d, max_len, visited, path, path_list, max_troops):
    path_length = 0
    # Mark the current node as visited and store in path
    visited[u] = True
    path.append(u)

    # If current vertex is same as destination, then print
    # current path[]
    if u == d or len(path) > max_len or path_weight(path, state) > max_troops:
        path_list.append(path)
        # print(path)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        path_list.append(copy.copy(path))
        for i in graph[u]:
            bool = True
            try:
                bool = visited[i]
            except:
                pass

            if not bool:
                printAllPathsUtil(state, graph, i, d, max_len, visited, path, path_list, max_troops)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[u] = False


def printAllPaths(state, graph, s, d, max_len, max_troops):
    path_list = []
    # Mark all the vertices as not visited
    visited = {}
    for key in graph.keys():
        visited[key] = False

    # Create an array to store paths
    path = []

    # Call the recursive helper function to print all paths
    printAllPathsUtil(state, graph, s, d, max_len, visited, path, path_list, max_troops)
    # print(len(path_list))
    return path_list


def choose_best_path(state, s, max_len, max_troops, player, d=None):
    board = state.board
    graph = board_to_graph_attacking_graph(board, player)
    path_list = printAllPaths(state, graph, s, d, max_len, max_troops)
    best_score = 0
    best_path = []
    for path in path_list:

        if is_legal_path(path, state, player):
            value = calculate_path_value(path, state, player)
            if value >= best_score:
                best_score = value
                best_path = path
    return best_path


def is_legal_path(path, state, player):
    for land in path:
        if land == path[0]:
            continue

        elif land.ruler == None or land.ruler.name == player.name:
            return False
    # print ("RETURN TRUE")
    return True
