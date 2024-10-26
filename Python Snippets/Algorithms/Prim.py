import heapq

def prim(graph, start):
    mst = []
    visited = set()
    min_heap = [(0, start, None)]

    while min_heap:
        weight, vertex, parent = heapq.heappop(min_heap)

        if vertex not in visited:
            visited.add(vertex)
            if parent is not None:
                mst.append((parent, vertex, weight))

            for neighbor, cost in graph[vertex]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (cost, neighbor, vertex))

    return mst
