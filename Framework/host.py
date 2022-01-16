from abc import ABC, abstractmethod


# The object that gets infected
class Host(ABC):

    def __init__(self):
        self._infected = False
        self._infectious = False
        self._latencyTime = 0
        self._infectedTime = 0
        self._immune = False

    @property
    def infectious(self):
        return self._infectious

    @property
    def latencyTime(self):
        return self._latencyTime

    @property
    def infectedTime(self):
        return self._infectedTime

    @property
    def immune(self):
        return self._immune

    @property
    def infected(self):
        return self._infected

    @infected.setter
    def infected(self, value):
        self._infected = value

    @latencyTime.setter
    def latencyTime(self, value):
        self._latencyTime = value

    @infectedTime.setter
    def infectedTime(self, value):
        self._infectedTime = value

    @immune.setter
    def immune(self, value):
        self._immune = value

    @infectious.setter
    def infectious(self, value):
        self._infectious = value

    @abstractmethod
    def increment(self, disease):
        pass

