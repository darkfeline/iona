from collections import deque


class Buffer:

    __slots__ = ['deque']

    def __init__(self):
        self.deque = deque()

    def __bool__(self):
        return bool(self.deque)

    def write(self, x):
        self.deque.append(x)

    def read(self):
        return self.deque.popleft()
