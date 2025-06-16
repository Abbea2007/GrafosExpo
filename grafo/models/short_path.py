#   Camino mas corto

from models.dijkstra import dijkstra

def shortest_path(graph, start, end):
    distances, previous_nodes = dijkstra(graph, start)
    path = []
    current = end

    while current in previous_nodes:
        path.insert(0, current)
        current = previous_nodes[current]

    if path:
        path.insert(0, start)

    return path, distances[end]
