import math
import random


def generate_points(n: int) -> list:
    random.seed(42)
    points = []
    for i in range(n):
        x = random.uniform(-100, 100)
        y = random.uniform(-100, 100)
        z = random.uniform(0, 50)
        points[i] = {"id": i, "x": x, "y": y, "z": z}
    return points


def get_cost(a: dict, b: dict, asymmetric: bool = False) -> float:
    if a["id"] == b["id"]:
        return float("inf")

    cost = math.sqrt((b["x"] - a["x"])**2 + (b["y"] - a["y"])**2 + (b["z"] - a["z"])**2)

    if asymmetric:
        if b["z"] > a["z"]:
            return 1.1 * cost
        if b["z"] < a["z"]:
            return 0.9 * cost

    return cost


def get_cost_matrix(points: list, asymmetric: bool = False, connections: float = 1.0) -> list:
    n = len(points)
    cost_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            cost_matrix[i][j] = get_cost(points[i], points[j], asymmetric)

    if connections < 1.0:
        random.seed(42)
        edges = [(i, j) for i in range(n) for j in range(n) if i != j]
        remove_amount = int(len(points) * (1.0 - connections))
        random_remove = random.sample(edges, remove_amount)
        for k, l in random_remove:
            cost_matrix[k][l] = float("inf")

    return cost_matrix
