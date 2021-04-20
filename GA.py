"""
    Module: GA
    Author: ShaoHaozhou
    motto: Self-discipline, self-improvement, self-love
    Date: 2020/12/23
    Introduce: The BP neural network can set the number of hidden layers,
            the number of neurons in each layer and the number of neurons in the output layer
    介绍: 可设置隐藏层的层数和每层神经元的数量、输出层的神经元数量的BP神经网络(实现自动化)
"""
import numpy as np
import matplotlib.pyplot as plt

"""
    GA:
        1. 离散GA
        2. 连续GA
"""


class GABase(object):
    def __init__(self, f, sv, cv):
        self.f = f
        self.sv = sv
        self.cv = cv
        self.pop = None
        self.best = [None, np.inf]
        self.fit_ = None
        self.for_ = None

    def initialize(self):
        pass

    def fitness(self):
        """
            # 用户可通过此函数来自定义目标函数...
                func(a_singe_pop) => return the fitness
        """
        return np.apply_along_axis(self.f, 1, self.pop)

    def select(self, fitness):
        min_pos = np.argmin(fitness)
        if fitness[min_pos] < self.best[1]:
            self.best = [self.pop[min_pos], fitness[min_pos]]

        min_fitness = fitness[min_pos]

        fitness = fitness - min_fitness
        u = np.sum(fitness)

        fitness = fitness / u

        s = 0
        for i in range(fitness.shape[0] - 1, -1, -1):
            a = fitness[i]
            fitness[i] = 1 - s
            s += a

        rands = np.random.rand(self.pop.shape[0] // 10)
        out = set()
        for rand in rands:
            for i in range(fitness.shape[0]):
                if rand < fitness[i]:
                    out.add(i)
                    break
        self.pop = np.delete(self.pop, list(out), axis=0)

    def cross(self):
        pass

    def mutate(self):
        pass

    def fit(self, for_=1000):
        self.fit_ = np.array([])
        self.for_ = for_
        self.best = [None, np.inf]
        self.initialize()
        for _ in range(for_):
            self.select(fitness=self.fitness())
            self.cross()
            self.mutate()
            self.fit_ = np.append(self.fit_, self.best[1])

    def draw_fit(self):
        if self.fit_ is None:
            raise ValueError("you should fit firstly!")
        x = np.linspace(0, self.for_, self.for_)
        y = self.fit_
        plt.plot(x, y)
        plt.show()


class DGA(GABase):
    def __init__(self, f, cv, sv, kinds, max_pop, length, can_replace=False):
        super().__init__(f, cv, sv)
        self.kinds = list(kinds)
        self.max_pop = max_pop
        self.length = length
        self.can_replace = can_replace

    def initialize(self):
        if self.can_replace is True:
            self.pop = np.random.choice(self.kinds, [self.max_pop // 10, self.length])
        else:
            self.pop = np.ones([self.max_pop // 10, self.length]) * np.inf
            for i in range(self.max_pop // 10):
                for j in range(self.length):
                    while True:
                        choice = np.random.choice(self.kinds)
                        if choice not in self.pop[i]:
                            self.pop[i][j] = choice
                            break

    def fitness(self):
        return super().fitness()

    def select(self, fitness):
        super().select(fitness)

    def cross(self):
        if self.can_replace is True:
            for i in range(self.pop.shape[0]):
                if self.max_pop <= self.pop.shape[0]:
                    break
                if np.random.rand() < self.sv:
                    selected = np.random.randint(self.length, size=[1, np.random.randint(self.length)])
                    child = self.pop[i].copy()
                    child[selected] = self.pop[(i+1) % self.pop.shape[0]][selected]
                    self.pop = np.vstack((self.pop, child))
        else:
            for i in range(self.pop.shape[0]):
                if self.max_pop <= self.pop.shape[0]:
                    break
                if np.random.rand() < self.sv:
                    selected = np.random.randint(self.length, size=[1, np.random.randint(self.length)])
                    child = self.pop[i].copy()
                    for j in selected[0]:
                        if child[j] == self.pop[(i+1) % self.pop.shape[0]][j]:
                            child[j] = self.pop[(i+1) % self.pop.shape[0]][j]

                    self.pop = np.vstack((self.pop, child))

    def mutate(self):
        if self.can_replace:
            for i in range(self.pop.shape[0]):
                if np.random.rand() < self.cv:
                    pos = np.random.randint(self.length)
                    self.pop[i][pos] = np.random.choice(self.kinds)
        else:
            for i in range(self.pop.shape[0]):
                if np.random.rand() < self.cv:
                    pos = np.random.randint(self.length)
                    while True:
                        cross = np.random.choice(self.kinds)
                        if cross not in self.pop[i]:
                            self.pop[i][pos] = cross
                            break

    def fit(self, for_=1000):
        super().fit(for_)

    def draw_fit(self):
        super().draw_fit()


class CGA(GABase):

    def __init__(self, f, sv, cv, max_pop, length, extent):
        super().__init__(f, sv, cv)
        self.max_pop = max_pop
        self.length = length
        self.extent = extent

    def initialize(self):
        self.pop = self.extent[0] + np.random.rand(self.max_pop // 10, self.length) * (self.extent[1] - self.extent[0])

    def fitness(self):
        return super().fitness()

    def select(self, fitness):
        super().select(fitness)

    def cross(self):
        for i in range(self.pop.shape[0]):
            if self.max_pop <= self.pop.shape[0]:
                break
            if np.random.rand() < self.sv:
                selected = np.random.randint(self.length, size=[1, np.random.randint(self.length)])
                child = self.pop[i].copy()
                child[selected] = self.pop[(i+1) % self.pop.shape[0]][selected]
                self.pop = np.vstack((self.pop, child))

    def mutate(self):
        for i in range(self.pop.shape[0]):
            if np.random.rand() < self.cv:
                pos = np.random.randint(self.length)
                self.pop[i][pos] = self.extent[0] + np.random.rand() * (self.extent[1] - self.extent[0])

    def fit(self, for_=1000):
        super().fit(for_)

    def draw_fit(self):
        super().draw_fit()


class GA(object):
    mode = ["DGA", "CGA"]

    def __init__(self, f, sv, cv, max_pop, length, extent_or_kinds, can_replace=False):
        if len(list(extent_or_kinds)) != 2:
            self.mode = GA.mode[0]
            self.ga = DGA(f, cv, sv, extent_or_kinds, max_pop, length, can_replace)
            self.msg = "{mode}(f:{f}, sv:{sv}, cv:{cv}, max_pop:{max_pop}," \
                       " length:{length}, kinds:{kinds}, can_replace{can_replace}"\
                .format(mode=self.mode, f=f, sv=sv, cv=cv, max_pop=max_pop, length=length, kinds=extent_or_kinds,can_replace=can_replace)
        else:
            self.mode = GA.mode[1]
            self.ga = CGA(f, cv, sv, max_pop, length, extent_or_kinds)
            self.msg = "{mode}(f:{f}, sv:{sv}, cv:{cv}, max_pop:{max_pop}," \
                       " length:{length}, extent:{extent})"\
                .format(mode=self.mode, f=f, sv=sv, cv=cv, max_pop=max_pop, length=length, extent=extent_or_kinds)

    def __repr__(self):
        return self.msg

    def __str__(self):
        return self.__repr__()

    def fit(self, for_=1000):
        self.ga.fit(for_)

    def result(self):
        return self.ga.best

    def draw_fit(self):
        self.ga.draw_fit()


if __name__ == "__main__":
    f = lambda x: sum(x * np.sin(x) + x * np.cos(2 * x))

    # 测试 DGA
    dga = DGA(f, cv=0.1, sv=0.01, kinds=np.linspace(0, 10, 100), max_pop=100, length=5)
    dga.fit(1000)
    dga.draw_fit()
    print(dga.best)

    # 测试 CGA
    cga = CGA(f, cv=0.1, sv=0.1, max_pop=100, length=5, extent=[0, 10])
    cga.fit(1000)
    cga.draw_fit()
    print(cga.best)

    # 测试 GA
    ga = GA(f, cv=0.1, sv=0.1, max_pop=100, length=5, extent_or_kinds=[0, 10])
    ga.fit(1000)
    ga.draw_fit()
