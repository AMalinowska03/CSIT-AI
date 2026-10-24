import random
import time


class Ant:
    def __init__(self, start: int):
        self.current_node = start
        self.path = [start]
        self.total_cost = 0.0

    def visit_node(self, next_node: int, cost: float):
        self.path.append(next_node)
        self.total_cost += cost
        self.current_node = next_node


def _run_single_aco(graph: list[list[float]], colony_size: int, random_choice_prob: float, evaporation_rate: float,
                    iterations: int = 100, alpha: float = 1.0, beta: float = 2.0, start: int = 0):
    n = len(graph)

    pheromone = [[1.0] * n for _ in range(n)]

    best_path = None
    best_cost = float('inf')

    for _ in range(iterations):
        ants = [Ant(start) for _ in range(colony_size)]

        for ant in ants:
            for _ in range(n - 1):
                current = ant.current_node
                unvisited = [c for c in range(n) if c not in ant.path]

                valid_neighbors = [c for c in unvisited if graph[current][c] != float('inf')]

                if not valid_neighbors:
                    break  # no paths to continue

                if random.random() < random_choice_prob:
                    next_node = random.choice(valid_neighbors)
                else:
                    probabilities = []
                    for neighbor in valid_neighbors:
                        tau = pheromone[current][neighbor] ** alpha
                        eta = (1.0 / graph[current][neighbor]) ** beta
                        probabilities.append(tau * eta)

                    total_prob = sum(probabilities)
                    if total_prob == 0:
                        next_node = random.choice(valid_neighbors)
                    else:
                        probabilities = [p / total_prob for p in probabilities]
                        next_node = random.choices(valid_neighbors, weights=probabilities, k=1)[0]

                ant.visit_node(next_node, graph[current][next_node])

            if len(ant.path) == n:
                return_cost = graph[ant.current_node][start]
                if return_cost != float('inf'):
                    ant.visit_node(start, return_cost)
                    if ant.total_cost < best_cost:
                        best_cost = ant.total_cost
                        best_path = tuple(ant.path)

        # evaporate pheromones
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1.0 - evaporation_rate)

        # update pheromones based on ants with complete paths
        for ant in ants:
            if len(ant.path) == n + 1:
                delta = 1.0 / ant.total_cost
                for k in range(len(ant.path) - 1):
                    u = ant.path[k]
                    v = ant.path[k + 1]
                    pheromone[u][v] += delta

    return best_path, best_cost


def aco(graph: list[list[float]], start: int = 0) -> dict:

    colony_sizes = [10, 20, 50]
    random_probs = [0.03, 0.1]
    evaporation_rates = [0.1, 0.5]

    overall_best_path = None
    overall_best_cost = float('inf')
    best_params = {
        "colony_size": None,
        "random_choice_probability": None,
        "evaporation_rate": None
    }
    search_time_of_best = None

    for colony_size in colony_sizes:
        for random_prob in random_probs:
            for evap_rate in evaporation_rates:
                starting_time = time.time()
                path, cost = _run_single_aco(
                    graph=graph,
                    colony_size=colony_size,
                    random_choice_prob=random_prob,
                    evaporation_rate=evap_rate,
                    iterations=50,
                    start=start
                )
                search_time = time.time() - starting_time

                if cost < overall_best_cost:
                    overall_best_cost = cost
                    overall_best_path = path
                    best_params = {
                        "colony_size": colony_size,
                        "random_choice_probability": random_prob,
                        "evaporation_rate": evap_rate
                    }
                    search_time_of_best = search_time

    return {
        "path": overall_best_path,
        "cost": overall_best_cost,
        "search_time": search_time_of_best,
        "params": best_params
    }