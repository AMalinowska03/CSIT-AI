from point_generator import generate_points, get_cost_matrix
from results import present_results
from algorithms.BFS import bfs
from algorithms.DFS import dfs
from algorithms.Dijkstra import dijkstra
from algorithms.NN import nearest_neighbours
from algorithms.Astar import a_star
from algorithms.ACO import aco


def run_experiment(asymmetric=False, connections=1.0):
    results = [{
        "city_count": i,
        "points": None,
        "graph": None,
        "BFS": {"path": None, "cost": float("inf"), "search_time": float("inf")},
        "DFS": {"path": None, "cost": float("inf"), "search_time": float("inf")},
        "Dijkstra": {"path": None, "cost": float("inf"), "search_time": float("inf")},
        "NN": {"path": None, "cost": float("inf"), "search_time": float("inf")},
        "A*": {"path": None, "cost": float("inf"), "search_time": float("inf")},
        "ACO": {"path": None, "cost": float("inf"), "search_time": float("inf"), "params": None},
    } for i in range(5, 21)]

    for city_count in range(5, 21):
        results_index = city_count - 5
        points = generate_points(city_count)
        graph = get_cost_matrix(points, asymmetric, connections)
        results[results_index]["points"] = points
        results[results_index]["graph"] = graph

        results[results_index]["BFS"] = bfs(graph)
        results[results_index]["DFS"] = dfs(graph)
        results[results_index]["Dijkstra"] = dijkstra(graph)
        results[results_index]["NN"] = nearest_neighbours(graph)
        results[results_index]["A*"] = a_star(graph)
        results[results_index]["ACO"] = aco(graph)
    present_results(results)


if __name__ == '__main__':
    run_experiment()
    run_experiment(True)
    run_experiment(False, 0.8)
    run_experiment(True, 0.8)
