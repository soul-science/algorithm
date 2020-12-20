import reprlib


class LineArray(list):
    """ Sum Tree """
    def __init__(self, iterable=[]):
        list.__init__([])
        self._initlize(iterable)

    def _initlize(self, iterable):
        self.extend(iterable)

    def getarray(self):
        return [self[i] if i == 0 else self[i] - self[i-1] for i in range(len(self))]

    def index(self, digit, start: int = ..., stop: int = ...):
        d = 0
        for i in range(len(self)):
            if i == 0:
                d = self[i]
            else:
                d = self[i] - self[i-1]
            if d == digit:
                return i
        return -1

    def count(self, digit):
        count = 0
        for i in range(len(self)):
            if i == 0:
                d = self[i]
            else:
                d = self[i] - d
            if d == digit:
                count += 1
        return count

    def sort(self, key=None, reverse=False):
        iterable = self.getarray()
        iterable.sort(key=key, reverse=reverse)
        self.clear()
        self._initlize(iterable)

    def insort(self, digit):   # 升序顺序插入
        for i in range(len(self)):
            if i == 0:
                d = self[i]
            else:
                d = self[i] - self[i-1]
            if digit <= d:
                break
            if i == len(self) - 1:
                i += 1

        self.insert(i, digit)

    def append(self, digit):
        if self == []:
            super(LineArray, self).append(digit)
        else:
            super(LineArray, self).append(self[-1] + digit)

    def extend(self, iterable):
        for digit in iterable:
            self.append(digit)

    def inextend(self, iterable):
        for digit in iterable:
            self.insort(digit)

    def pop(self, index=None):
        if index is None:
            popitem = self.iterable.pop()
            super().pop()
        else:
            popitem = self.iterable.pop(index)
            super().pop(index)

            for i in range(index, len(self.iterable)):
                self[i] -= - popitem

        return popitem

    def remove(self, digit):
        index = self.index(digit)
        self.iterable.remove(digit)
        super().pop(index)

        for i in range(index, len(self.iterable)):
            self[i] -= - popitem

    def insert(self, index: int, digit):
        if index == 0:
            super().insert(index, digit)
        else:
            super().insert(index, self[index-1] + digit)
        for i in range(index + 1, len(self)):
            self[i] += digit

    def clear(self):
        super().clear()

    def copy(self):
        return LineArray(self.getarray())

    def __repr__(self):
        return reprlib.repr("LineArray(" + super().__repr__() + ")")

    def __str__(self):
        return self.__repr__()

    def __sort__(self, key=None, reverse=False):
        new = LineArray(iterable=sorted(self.getarray()))
        new.sort(key, reverse)
        return new
