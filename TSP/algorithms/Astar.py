import heapq
import time


def a_star(graph, start=0, admissible=True):
    n = len(graph)
    best_cost = float('inf')
    best_path = None

    min_path_cost, max_path_cost = find_min_max_costs(graph)

    def heuristic(visited_count):
        remaining_count = len(graph) - visited_count + 1
        if admissible:
            return remaining_count * min_path_cost
        else:
            return remaining_count * max_path_cost

    priority_queue: list[tuple[float, float, int, tuple[int, ...]]] = [(0.0+heuristic(1), 0.0, start, (start,))]

    starting_time = time.time()
    while priority_queue:
        approximate_cost, current_cost, current_node, path = heapq.heappop(priority_queue)

        if len(path) == n:
            return_cost = graph[current_node][start]
            if return_cost != float('inf'):  # no return path to starting city, rejected path
                best_cost = current_cost + return_cost
                best_path = path + (start,)
                search_time = time.time() - starting_time
                # returning first full path because heapq pops out node with the lowest estimated total cost (f = g + h)
                return {"path": best_path, "cost": best_cost, "search_time": search_time}
            continue

        for next_node in range(n):
            if next_node not in path and graph[current_node][next_node] != float('inf'):
                next_cost = current_cost + graph[current_node][next_node]
                next_approximate_cost = next_cost + heuristic(len(path)+1)
                heapq.heappush(priority_queue, (next_approximate_cost, next_cost, next_node, path + (next_node,)))

    search_time = time.time() - starting_time
    return {"path": best_path, "cost": best_cost, "search_time": search_time}


def find_min_max_costs(graph):
    valid_paths = [
        graph[i][j]
        for i in range(len(graph))
        for j in range(len(graph))
        if i != j and graph[i][j] != float('inf')
    ]

    if not valid_paths:
        return 0.0, 0.0

    return min(valid_paths), max(valid_paths)
