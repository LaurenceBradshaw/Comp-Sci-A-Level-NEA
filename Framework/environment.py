from abc import ABC, abstractmethod
import people


# The object that contains hosts
class Environment(ABC):

    def __init__(self, name, activePeriod, infectionMultiplier):
        self._activePeriod = activePeriod
        self._hosts = []
        self._infectionMultiplier = infectionMultiplier
        self._name = name

    @property
    def activePeriod(self):
        return self._activePeriod

    @property
    def hosts(self):
        return self._hosts

    @property
    def infectionMultiplier(self):
        return self._infectionMultiplier

    @property
    def name(self):
        return self._name

    @activePeriod.setter
    def activePeriod(self, value):
        self._activePeriod = value

    @hosts.setter
    def hosts(self, value):
        self._hosts = value

    @infectionMultiplier.setter
    def infectionMultiplier(self, value):
        self._infectionMultiplier = value

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def timeStep(self, disease, day):
        pass

