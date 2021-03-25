import numpy as np
import matplotlib.pyplot as plt


class Pso(object):
    def __init__(self, f, i, extent, lr=0.01, c1=0.5, c2=0.5, vt=15, vm=-15, al=50):
        self.f = f
        self.extent = extent
        self.w = None
        self.lr = lr
        self.al_x = extent[0] + np.random.rand(al, i) * (extent[1] - extent[0])
        self.al_v = np.random.randn(al, i)
        self.al_best_e = np.zeros(al)
        self.al_best_x = np.zeros((al, i))
        self.best_e = 0
        self.best_x = np.zeros((1, i))
        self.v = [vm, vt]
        self.c = [c1, c2]

    def evaluate(self):
        return np.apply_along_axis(self.f, 1, self.al_x)  # axis=0 对每列进行函数运算; axis=1 对每行进行函数运算

    def iterate(self, evaluations, batch):
        if batch != 0:
            for i in range(evaluations.shape[0]):
                if evaluations[i] < self.al_best_e[i]:
                    self.al_best_e[i] = evaluations[i]
                    self.al_best_x[i] = self.al_x[i]

            dm = np.argmin(self.al_best_e)
            if self.best_e > self.al_best_e[dm]:
                self.best_e = self.al_best_e[dm]
                self.best_x = self.al_best_x[dm]

        else:
            self.al_best_e = evaluations
            self.al_best_x = np.copy(self.al_x)
            dm = np.argmin(self.al_best_e)
            self.best_e = self.al_best_e[dm]
            self.best_x = self.al_best_x[dm]

        for i in range(evaluations.shape[0]):
            self.al_v[i] = self.w(batch)*self.al_v[i] + np.random.ranf() * self.c[0] * (self.al_best_x[i] - self.al_x[i]) \
                           + self.c[1] * np.random.ranf() * (self.best_x - self.al_x[i])

            self.al_v[i][self.al_v[i] < self.v[0]] = self.v[0]
            self.al_v[i][self.al_v[i] > self.v[1]] = self.v[1]

            self.al_x[i] = self.al_x[i] + self.al_v[i]

            self.al_x[i][self.al_x[i] < self.extent[0]] = self.extent[0]
            self.al_x[i][self.al_x[i] > self.extent[1]] = self.extent[1]

    def fit(self, for_=10000):
        self.w = lambda w: (1 + 1 / for_ * 2) ** (-w)

        for i in range(for_):
            evaluations = self.evaluate()
            self.iterate(evaluations, i)

    def result(self):
        return [self.best_x, self.best_e]


def draw(f, extent, point, interval):
    x = np.linspace(extent[0], extent[1], interval)
    y = f(x)
    plt.plot(x, y)
    plt.plot(point[0], point[1], 'ro')
    plt.show()


if __name__ == '__main__':
    import time
    f1 = lambda x: x * np.sin(x) + x * np.cos(2*x)
    # f1 = lambda x: x * np.sin(x)**2 - x * np.cos(x)**2
    # f1 = lambda x: np.log(x + 1) - x * np.cos(x)
    pso = Pso(f1, 1, [0, 10], al=10)
    t = time.time()
    pso.fit(10)
    print(time.time() - t)
    x, y = pso.result()
    print(x, y)
    draw(f1, [0, 10], [x, y], 1000)