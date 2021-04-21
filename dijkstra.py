import numpy as np


# 广义的dijkstra
def dijkstra(start, end, matrix, is_undigraph=True):
    d = dict()
    if is_undigraph is True:
        for each in matrix:
            keys = list(d.keys())
            if each[0] not in keys:
                d[each[0]] = set()
            d[each[0]].add((each[1], each[2]))
            if each[1] not in keys:
                d[each[1]] = set()
            d[each[1]].add((each[0], each[2]))
    else:
        for each in matrix:
            keys = list(d.keys())
            if each[0] not in keys:
                d[each[0]] = set()
            d[each[0]].add((each[1], each[2]))
            if d[each[1]] not in keys:
                d[each[1]] = set()

    path = []
    rest = []
    for i in range(max(d)+1):
        path.append([[], 0])
        if i != start:
            rest.append(0)
        else:
            rest.append(1)
    path[start][0].append(start)
    current = np.ones(max(d) + 1) * np.inf
    current[start] = 0
    now = start
    while now != end:
        for each in d[now]:
            if rest[each[0]] == 0 and each[1] + current[now] < current[each[0]]:
                current[each[0]] = each[1] + current[now]
                path[each[0]][0] = path[now][0]
                path[each[0]][1] += each[1]
        for i in range(len(current)):
            if rest[i] == 0 and (rest[now] == 1 or current[now] >= current[i]):
                now = i

        rest[now] = 1
        path[now][0].append(now)

    return path[now]
