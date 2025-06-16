from models.grafo import get_graph
from models.short_path import shortest_path

def main():
    graph = get_graph()
    start = 'A'
    end = 'E'
    path, total_time = shortest_path(graph, start, end)

    print("Camino más corto:", " -> ".join(path))
    print(f"Tiempo total: {total_time} minutos")

if __name__ == "__main__":
    main()
