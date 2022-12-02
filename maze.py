from operator import ne
import random
from collections import deque
from queue import Queue, PriorityQueue
from heapq import heappop, heappush


def create_maze():
    w, h = 20, 20
    maze = [[0 for x in range(w)] for y in range(h)]
    for i in range(20):
        for j in range(20):
            maze[i][j] = '.'
    maze[0][0] = 'p'
    maze[15][15] = '*'
    maze[3][6] = '*'
    p = 0
    w = 0
    while (w != 80):
        wall_x = random.randint(0, 19)
        wall_y = random.randint(0, 19)
        if (maze[wall_x][wall_y] == '.' and (wall_x != 0 and wall_y != 1) and (wall_x != 2 and wall_y != 6) and (wall_x != 4 and wall_y != 6) and (wall_x != 14 and wall_y != 15) and (wall_x != 16 and wall_y != 15)):
            maze[wall_x][wall_y] = '|'
            w += 1
    return maze


def maze2graph(maze):
    height = 20
    width = 20
    graph = {(i, j): [] for j in range(width)
             for i in range(height)}
    for row, col in graph.keys():
        if(maze[row][col] != '|'):
            if(row == 0 and col == 0):  # (0,0)
                if(maze[row+1][col] == '.'):
                    graph[(row, col)].append(("S", (row+1, col)))
                if(maze[row][col+1] == '.'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(row == 0 and col == 19):  # (0,19)
                if(maze[row][col-1] == '.'):
                    graph[(row, col)].append(("W", (row, col-1)))
                if(maze[row+1][col] == '.'):
                    graph[(row, col)].append(("S", (row + 1, col)))

            if(row == 19 and col == 0):
                if(maze[row - 1][col] == '.'):
                    graph[(row, col)].append(("N", (row-1, col)))
                if(maze[row][col+1] == '.'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(row == 19 and col == 19):
                if(maze[row - 1][col] == '.'):
                    graph[(row, col)].append(("N", (row-1, col)))
                if(maze[row][col-1] == '.'):
                    graph[(row, col)].append(("W", (row, col-1)))

            if(row == 0 and col != 19 and col != 0):
                if(maze[row][col-1] == '.'):
                    graph[(row, col)].append(("W", (row, col-1)))
                if(maze[row+1][col] == '.'):
                    graph[(row, col)].append(("S", (row + 1, col)))
                if(maze[row][col+1] == '.'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(0 < row < 19 and 0 < col < 19):
                if(maze[row+1][col] == '.' or maze[row+1][col] == '*'):
                    graph[(row, col)].append(("S", (row+1, col)))
                if(maze[row-1][col] == '.' or maze[row-1][col] == '*'):
                    graph[(row, col)].append(("N", (row - 1, col)))
                if(maze[row][col-1] == '.' or maze[row][col-1] == '*'):
                    graph[(row, col)].append(("W", (row, col-1)))
                if(maze[row][col+1] == '.' or maze[row][col+1] == '*'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(row == 19 and col != 19 and col != 0):
                if(maze[row][col-1] == '.'):
                    graph[(row, col)].append(("W", (row, col-1)))
                if(maze[row-1][col] == '.'):
                    graph[(row, col)].append(("N", (row - 1, col)))
                if(maze[row][col+1] == '.'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(col == 0 and row != 19 and row != 0):
                if(maze[row+1][col] == '.'):
                    graph[(row, col)].append(("S", (row+1, col)))
                if(maze[row-1][col] == '.'):
                    graph[(row, col)].append(("N", (row - 1, col)))
                if(maze[row][col+1] == '.'):
                    graph[(row, col)].append(("E", (row, col+1)))

            if(col == 19 and row != 19 and row != 0):
                if(maze[row+1][col] == '.'):
                    graph[(row, col)].append(("S", (row+1, col)))
                if(maze[row-1][col] == '.'):
                    graph[(row, col)].append(("N", (row - 1, col)))
                if(maze[row][col-1] == '.'):
                    graph[(row, col)].append(("W", (row, col-1)))

    return graph


def find_path_ucs(maze):
    start = (0, 0)
    goal = (3, 6)
    frontier = PriorityQueue()
    frontier.put((0, "", start))
    explored = set()
    number_of_nodes_visited = 0
    graph = maze2graph(maze)
    while frontier:
        ucs_w, path, current = frontier.get()
        if current not in explored:
            explored.add(current)
            number_of_nodes_visited += 1
        if current == goal:
            return path, number_of_nodes_visited
        for direction, neighbour in graph[current]:
            if neighbour not in explored:
                ucs_w += 1
                frontier.put((ucs_w, direction + path, neighbour))
            i = 0
            if maze[neighbour[i]][neighbour[i+1]] == '.':
                maze[neighbour[i]][neighbour[i+1]] = 'E'
    return "No way Exception"


def find_path_dfs(maze):
    start, goal = (0, 0), (3, 6)
    frontier = deque([("", start)])
    visited = set()
    cost = 0
    graph = maze2graph(maze)
    while frontier:
        path, current = frontier.pop()
        if current == goal:
            return path, cost
        if current in visited:
            continue
        visited.add(current)
        cost += 1
        for direction, neighbour in graph[current]:
            frontier.append((path + "  " + direction, neighbour))

        for i, j in visited:
            # i = 0
            if maze[i][j] == '.':
                maze[i][j] = 'E'
    return "NO WAY!", cost


w, h = 20, 20
maze = [[0 for x in range(w)] for y in range(h)]
maze = create_maze()
for i in maze:
    for j in i:
        print(j, end=" ")
    print()

#################     PRINT MAZW2GRAPH     ##################

# graph = {(i, j): [] for j in range(20)
#          for i in range(20)}
# graph = maze2graph(maze)
# print(graph)

# ************YOU CAN EXECUTE EACH ALGORITHM SEPERATLY
##########################   DFS ALGORITHM     ########################

# path_dfs, number_of_nodes_visited_dfs = find_path_dfs(maze)
# search_cost_dfs = 0
# for j in range(number_of_nodes_visited_dfs):
#     search_cost_dfs = search_cost_dfs + j
# print('search cost dfs: ' + str(search_cost_dfs))
# print("path dfs: " + path_dfs)
# print('number of nodes visited dfs: ' + str(number_of_nodes_visited_dfs))

##########################   UCS ALGORITHM     ########################
path_ucs, number_of_nodes_visited_ucs = find_path_ucs(maze)
search_cost_ucs = 0
for i in range(number_of_nodes_visited_ucs):
    search_cost_ucs = search_cost_ucs + i
print('search cost ucs: ' + str(search_cost_ucs))
print("path ucs: " + path_ucs)
print('number of nodes visited ucs : ' + str(number_of_nodes_visited_ucs))
