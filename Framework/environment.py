from abc import ABC, abstractmethod


class Environment(ABC):
    """
    Abstract class for the place where the hosts are
    """

    def __init__(self, name, activePeriod, interactionRate):
        """
        Constructor for an environment
        
        :param name: Name for the environment
        :param activePeriod: The days/times when the hosts are in the environment and can infect each other/be infected
        :param interactionRate: The amount the hosts mix with one another (determines the number of interactions)
        """
        self._activePeriod = activePeriod
        self._hosts = []
        self._interactionRate = interactionRate
        self._name = name

    @property
    def activePeriod(self):
        return self._activePeriod

    @property
    def hosts(self):
        return self._hosts

    @property
    def interactionRate(self):
        return self._interactionRate

    @property
    def name(self):
        return self._name

    @activePeriod.setter
    def activePeriod(self, value):
        self._activePeriod = value

    @hosts.setter
    def hosts(self, value):
        self._hosts = value

    @interactionRate.setter
    def interactionRate(self, value):
        self._interactionRate = value

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def timeStep(self, disease, day):
        pass

    @abstractmethod
    def getInfectedCount(self):
        # returns the number of infected hosts
        count = 0
        for h in self.hosts:
            if h.infected:
                count += 1
        return count

    @abstractmethod
    def getImmuneCount(self):
        # Returns the number of immune hosts
        count = 0
        for h in self.hosts:
            if h.immune:
                count += 1
        return count

