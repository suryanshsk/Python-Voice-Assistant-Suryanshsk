def warshall(graph):
    V = len(graph)
    reach = [[0]*V for _ in range(V)]

    for i in range(V):
        for j in range(V):
            reach[i][j] = graph[i][j]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])

    return reach
