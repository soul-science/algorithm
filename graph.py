from array import array
import reprlib
from math import inf


class Graph:
    step_method = []
    path_method = []
    tree_method = []

    def __init__(self, graph, typed='d'):
        self.typed = typed
        self.length = 0
        self.graph = []
        if self.__is_graph(graph) is False:
            raise Exception("The rect is not graph !!!")
        self.__initlize(graph)

    def __repr__(self):
        return reprlib.repr("Graph(" + str([e.tolist() for e in self.graph]) + ",typed=" + self.typed + ")")

    def __str__(self):
        return self.__repr__()

    def __initlize(self, graph):
        graph = [array(self.typed, line) for line in graph]
        self.length = len(graph)
        self.graph = graph

    def get_min_steps(self, start, end, method=None):
        if method not in self.step_method:
            raise Exception("The method not in step_method")

        return eval("self._" + method + "(" + str(start) + "," + str(end) + ")")

    def get_min_path(self, start, end, method=None):
        if method not in self.path_method:
            raise Exception("The method not in path_method")

        return eval("self._" + method + "(" + str(start) + "," + str(end) + ")")

    def get_min_tree(self, method=None):
        if method not in self.tree_method:
            raise Exception("The method not in tree_method")

        return eval("self._" + method + "()")

    def __is_graph(self, graph, offset=0):
        flag = True
        length = len(graph[0])
        for i in range(len(graph)):
            if length != len(graph[i]) and graph[i][i + offset] != 0:
                flag = False
                break

        return flag

    def append(self, line, tolines):
        if len(tolines) != self.length:
            raise Exception("The length of tolines is not equal with graph !")
        if len(line) != self.length + 1:
            raise Exception("The add_line is not equal with others !")
        elif line[self.length] != 0:
            raise Exception("The add_line's Distance to its own node is not 0 !")
        else:
            self.graph.append(array(self.typed, line))

        for i in range(len(tolines)):
            self.graph[i].append(tolines[i])

        self.length += 1

    def __append(self, lines, tolines):
        length = len(lines)
        for i in range(length):
            self.graph.append(array(self.typed, lines[i]))

            for j in range(self.length):
                self.graph[j].append(tolines[i][j])

        self.length += length

    def pop(self, index=None):
        if index is None:
            popitem = self.graph.pop()
            for line in self.graph:
                line.pop()
        else:
            popitem = self.graph.pop(index)
            for line in self.graph:
                line.pop(index)
        return popitem

    def extend(self, lines, tolines):
        if len(lines) != len(tolines):
            raise Exception("The length of lines is not equal with tolines !")

        if self.__is_graph(lines, offset=self.length) is False:
            raise Exception("The lines is not graph !!!")

        for line in tolines:
            if len(line) != self.length:
                raise Exception("The toline" + str(line) + " is out of length !")

        self.__append(lines, tolines)

    def reset(self, graph, typed=None):
        self.graph.clear()
        self.length = 0
        self.typed = typed if typed is not None else self.typed

        self.__initlize(graph)


class Undigraph(Graph):
    step_method = ['dijkstra']
    path_method = ['dfs', 'bfs']
    tree_method = ['prim', 'kruskal']

    def __init__(self, graph, typed='d'):
        if self.__is_graph(graph) is False:
            raise Exception("The rect is not graph !!!")
        else:
            super().__init__(graph, typed)
        self.__min_tree = []
        self.__all_path = []
        self.__vis = []
        self.__path = []
        self.__end = 0

    def __is_graph(self, graph, offset=0):
        length = len(graph)
        for i in range(length):
            for j in range(length):
                if graph[i + offset][j] != graph[j][i + offset]:
                    return False
        return True

    def _dfs(self, start, end):
        self.__vis = [0]*self.length
        self.__path.clear()
        self.__all_path.clear()
        self.__path.append(start)
        self.__end = end
        self.__vis[start] = 1
        self.__dfs(start)

        return self.__all_path

    def __dfs(self, current):
        if current == self.__end:
            self.__all_path.append(self.__path.copy())
            return

        for i in range(self.length):
            if self.__vis[i] == 0 and self.graph[current][i] != inf:
                self.__vis[i] = 1
                self.__path.append(i)
                self.__dfs(i)
                self.__vis[i] = 0
                self.__path.pop()

    def _bfs(self, start, end):
        self.__all_path.clear()
        self.__path.clear()
        self.__end = end
        self.__bfs(start, [start])

        return self.__all_path

    def __bfs(self, current, path):
        if current == self.__end:
            self.__all_path.append(path)
            return

        for i in range(self.length):
            if i not in path and self.graph[current][i] != inf:
                path.append(i)
                self.__bfs(i, path.copy())
                path.pop()

    def _prim(self):
        self.__vis = [0]*self.length
        self.__path.clear()
        self.__min_tree.clear()
        self.__path = [0]*self.length
        self.__vis[0] = 1
        current = 0
        for _ in range(self.length - 1):
            for i in range(self.length):
                if self.__vis[i] == 0 and self.graph[current][i]:
                    if self.__path[i] == 0:
                        self.__path[i] = (current, i, self.graph[current][i])
                    elif self.__path[i][2] > self.graph[current][i]:
                        self.__path[i] = (current, i, self.graph[current][i])
            Min = [0, inf]
            for i in range(self.length):
                if self.__vis[i] == 0 and self.__path[i][2] < Min[1]:
                    Min = [i, self.__path[i][2]]
            if Min[1] == inf:
                return -1
            self.__min_tree.append(self.__path[Min[0]])
            self.__vis[Min[0]] = 1

        return self.__min_tree

    def _kruskal(self):
        self.__min_tree.clear()
        self.__all_path.clear()
        v = set()
        for i in range(self.length):
            for j in range(self.length):
                if i != j:
                    self.__all_path.append((i, j, self.graph[i][j]))

        while len(v) < self.length:
            Min = min(self.__all_path, key=lambda x: x[2])
            length = len(v)
            v.add(Min[0])
            v.add(Min[1])
            if len(v) > length:
                self.__min_tree.append(Min)
            self.__all_path.remove(Min)

        return self.__min_tree

    def _dijkstra(self, start, end):
        self.__path = [[[], inf] for _ in range(self.length)]
        self.__vis = [0] * self.length
        self.__path[start] = [[start], 0]
        self.__vis[start] = 1
        current = start
        while self.__vis.index(0) != -1:
            for i in range(self.length):
                if self.__vis[i] == 0 and self.__path[i][1] > self.__path[current][1] + self.graph[current][i]:
                    self.__path[i][0] = self.__path[current][0].copy()
                    self.__path[i][1] = self.__path[current][1] + self.graph[current][i]
            Min = [0, inf]
            for i in range(self.length):
                if self.__vis[i] == 0 and self.__path[i][1] < Min[1]:
                    Min = [i, self.__path[i][1]]
            self.__path[Min[0]][0].append(Min[0])
            if Min[1] == inf:
                return -1
            if Min[0] == end:
                return self.__path[end]
            self.__vis[Min[0]] = 1
            current = Min[0]

    def get_min_steps(self, start, end, method='dijkstra'):
        return super().get_min_steps(start, end, method)

    def get_min_path(self, start, end, method='dfs'):
        return super().get_min_path(start, end, method)

    def get_min_tree(self, method='prim'):
        return super().get_min_tree(method)


class Digraph(Graph):
    def __init__(self, graph, typed='d'):
        super().__init__(graph, typed)

    def get_min_steps(self, start, end, method=None):
        pass

    def get_min_path(self, start, end, method=None):
        pass

    def get_min_tree(self, method=None):
        pass
