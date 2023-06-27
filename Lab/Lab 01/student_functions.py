import numpy as np
from collections import deque
from queue import PriorityQueue


def DFS(matrix, start, end):
    """
    BFS algorithm:
    Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes, each key is a visited node,
        each value is the adjacent node visited before it.
    path: list
        Founded path
    """

    if start < 0 or end >= len(matrix):
        print("Invalid Inputs: start and/or end out of range")
        return {}, []

    visited = {start: None}
    visited = dfs_recursive(matrix, visited, start, end)
    path = visited_to_path_converter(visited, end)

    return visited, path


def dfs_recursive(matrix, visited, current, end):
    if current == end:
        return visited

    for vertex in range(len(matrix)):
        cost = matrix[current][vertex]
        if cost > 0 and vertex not in visited:
            visited[vertex] = current
            visited = dfs_recursive(matrix, visited, vertex, end)

    return visited


def BFS(matrix, start, end):
    """
    DFS algorithm
     Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited 
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """

    if start < 0 or end >= len(matrix):
        print("Invalid Inputs: start and/or end out of range")
        return {}, []

    visited = {start: None}
    queue = deque()
    queue.append(start)

    while 1:
        current = queue.popleft()
        if current == end:
            break

        for vertex in range(len(matrix)):
            cost = matrix[current][vertex]
            if cost > 0 and vertex not in visited:
                visited[vertex] = current
                queue.append(vertex)
                if vertex == end:
                    break

    path = visited_to_path_converter(visited, end)
    return visited, path


def UCS(matrix, start, end):
    """
    Uniform Cost Search algorithm
     Parameters:visited
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
    
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    if start < 0 or end >= len(matrix):
        print("Invalid Inputs: start and/or end out of range")
        return {}, []

    visited = {start: None}
    queue = PriorityQueue()
    queue.put((0, start))

    while queue.not_empty:
        current = queue.get()
        current_cost = current[0]
        current_node = current[1]

        for vertex in range(len(matrix)):
            cost = matrix[current_node][vertex]
            if cost <= 0:
                continue
            if vertex in visited:
                temp_path = visited_to_path_converter(visited, vertex)
                temp_cost = path_cost_calc(matrix, temp_path)
                if current_cost + cost < temp_cost:
                    visited[vertex] = current_node
                    queue.put((current_cost + cost, vertex))
                continue

            if vertex not in visited:
                queue.put((current_cost + cost, vertex))
                visited[vertex] = current_node

        if current_node == end:
            break

    path = visited_to_path_converter(visited, end)

    return visited, path


def GBFS(matrix, start, end):
    """
    Greedy Best First Search algorithm
     Parameters:
    ---------------------------
    matrix: np array 
        The graph's adjacency matrix
    start: integer 
        starting node
    end: integer
        ending node
   
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node, 
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """

    # Reference
    # Greedy Best First Search | Quick Explanation with Visualization: https://www.youtube.com/watch?v=dv1m3L6QXWs
    # Best First Search (Informed Search): https://www.geeksforgeeks.org/best-first-search-informed-search/

    if start < 0 or end >= len(matrix):
        print("Invalid Inputs: start and/or end out of range")
        return {}, []

    visited = {start: None}
    queue = PriorityQueue()
    queue.put((0, start))

    while queue.not_empty:
        current = queue.get()[1]
        if current == end:
            break
        for vertex in range(len(matrix)):
            cost = matrix[current][vertex]
            if cost > 0 and vertex not in visited:
                visited[vertex] = current
                queue.put((cost, vertex))

    path = visited_to_path_converter(visited, end)

    return visited, path


def Astar(matrix, start, end, pos):
    visited = {start: None}
    path = []
    open_list = PriorityQueue()
    open_list.put((0, start))
    closed_list = []
    flag = False

    while True:
        if open_list.empty():
            return visited, path

        current = open_list.get()[1]
        closed_list.append(current)
        if current == end:
            break

        for vertex in range(len(matrix)):
            cost = matrix[current][vertex]
            if cost > 0 and vertex not in visited and vertex not in closed_list:
                visited[vertex] = current
                if vertex == end:
                    flag = True
                    break

                previous_node = visited[vertex]
                path.append(vertex)
                if previous_node is not None:
                    path.append(previous_node)
                while previous_node in visited and previous_node is not None:
                    previous_node = visited[previous_node]
                    if previous_node is not None:
                        path.append(previous_node)
                path.reverse()

                g = 0
                for i in range(len(path) - 1):
                    g += matrix[path[i]][path[i + 1]]

                h = np.sqrt((pos[end][0] - pos[vertex][0]) ** 2 + (pos[end][1] - pos[vertex][1]) ** 2)
                f = g + h
                if vertex not in list(open_list.queue):
                    open_list.put((f, vertex))

        if flag:
            break

    path.clear()
    previous_node = visited[end]
    path.append(end)
    if previous_node is not None:
        path.append(previous_node)
    while previous_node in visited and previous_node is not None:
        previous_node = visited[previous_node]
        if previous_node is not None:
            path.append(previous_node)
    path.reverse()

    return visited, path


def visited_to_path_converter(visited, end):
    path = []
    if end not in visited:
        print('Path not found!!!')
        return visited, path

    previous_node = visited[end]
    path.append(end)
    if previous_node is not None:
        path.append(previous_node)
    while previous_node in visited and previous_node is not None:
        previous_node = visited[previous_node]
        if previous_node is not None:
            path.append(previous_node)

    path.reverse()

    return path


def path_cost_calc(matrix, path):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += matrix[path[i]][path[i + 1]]
    return total_cost


def euclidean_distance(pos1, pos2):
    return np.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
