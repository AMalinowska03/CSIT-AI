import heapq
import time


def dijkstra(graph, start=0):
    n = len(graph)
    best_cost = float('inf')
    best_path = None

    priority_queue: list[tuple[float, int, tuple[int, ...]]] = [(0.0, start, (start,))]

    starting_time = time.time()
    while priority_queue:
        current_cost, current_node, path = heapq.heappop(priority_queue)

        if len(path) == n:
            return_cost = graph[current_node][start]
            if return_cost != float('inf'):  # no return path to starting city, rejected path
                best_cost = current_cost + return_cost
                best_path = path + (start,)
                search_time = time.time() - starting_time
                # returning first full path because heapq pops out node with the lowest cumulative cost
                return {"path": best_path, "cost": best_cost, "search_time": search_time}
            continue

        for next_node in range(n):
            if next_node not in path and graph[current_node][next_node] != float('inf'):
                next_cost = current_cost + graph[current_node][next_node]
                heapq.heappush(priority_queue, (next_cost, next_node, path + (next_node,)))

    search_time = time.time() - starting_time
    return {"path": best_path, "cost": best_cost, "search_time": search_time}
