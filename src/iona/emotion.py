import abc
import math


class Emotion(metaclass=abc.ABCMeta):

    def __init__(self, value=0):
        self._value = value

    @property
    def value(self):
        """Get emotion value"""
        return self._value

    def dump(self):
        """Get raw value

        This value should create an identical object when passed into the
        constructor.

        """
        return self._value

    @abc.abstractmethod
    def decay(self, dt):
        """Decay emotion naturally by dt seconds"""

    def increase(self, value):
        """Increase emotion by non-negative value"""
        assert value >= 0
        self._value += value

    def decrease(self, value):
        """Increase emotion by non-negative value"""
        assert value >= 0
        self._value -= value


class Happiness(Emotion):

    def __init__(self, value=0):
        super().__init__(value)
        self._timeout = 0
        self._buffer = 0

    @property
    def value(self):
        return self._value / (abs(self._value)+100)

    def decay(self, dt):
        self._value -= dt/2

    def increase(self, value):
        super().increase(value)
        self._timeout = value
        self._buffer = value

    def decrease(self, value):
        super().decrease(value)
        self._timeout = math.log(value)
        if self._timeout < 0:
            self._timeout = 0
            self._buffer = 0
        else:
            self._buffer = math.log(value)
