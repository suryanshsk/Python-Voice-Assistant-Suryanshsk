def bellman_ford(graph, start):
    distance = {v: float('inf') for v in graph}
    distance[start] = 0

    for _ in range(len(graph) - 1):
        for u in graph:
            for v, w in graph[u]:
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w

    for u in graph:
        for v, w in graph[u]:
            if distance[u] + w < distance[v]:
                print("Graph contains negative weight cycle")
                return None

    return distance
