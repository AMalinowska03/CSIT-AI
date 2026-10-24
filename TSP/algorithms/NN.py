import time


def nearest_neighbours(graph, start=0):
    n = len(graph)

    current_node = start
    taken_path = (start,)
    visited = {start}
    total_cost = 0.0

    starting_time = time.time()

    for _ in range(n-1):
        nearest_found_node = None
        lowest_found_cost = float('inf')

        for next_node in range(n):
            next_path_cost = graph[current_node][next_node]
            if next_node not in visited and next_path_cost != float('inf'):
                if next_path_cost < lowest_found_cost:
                    lowest_found_cost = next_path_cost
                    nearest_found_node = next_node

        if nearest_found_node is None:
            return {"path": None, "cost": float("inf"), "search_time": time.time() - starting_time}

        visited.add(nearest_found_node)
        taken_path += (nearest_found_node,)
        total_cost += lowest_found_cost
        current_node = nearest_found_node

    return_cost = graph[current_node][start]
    if return_cost == float('inf'):
        return {"path": None, "cost": float("inf"), "search_time": time.time() - starting_time}

    taken_path += (start,)
    total_cost += return_cost
    return {"path": taken_path, "cost": total_cost, "search_time": time.time() - starting_time}


