from collections import deque
import time


def bfs(graph, start=0):
    n = len(graph)
    best_cost = float('inf')
    best_path = None

    # current city we're in, path taken there, cost of that path
    queue: deque[tuple[int, tuple[int, ...], float]] = deque([(start, (start,), 0.0)])

    starting_time = time.time()
    while queue:
        current_node, path, current_cost = queue.popleft()

        if len(path) == n:
            return_cost = graph[current_node][start]
            if return_cost != float('inf'):  # no return path to starting city, rejected path
                path_cost = current_cost + return_cost
                if path_cost < best_cost:
                    best_cost = path_cost
                    best_path = path + (start,)
            continue  # this point is a leaf, we move on to another

        for next_node in range(n):
            if next_node not in path and graph[current_node][next_node] != float('inf'):
                queue.append((next_node, path + (next_node, ), current_cost + graph[current_node][next_node]))

    search_time = time.time() - starting_time
    return {"path": best_path, "cost": best_cost, "search_time": search_time}
