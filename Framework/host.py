from abc import ABC, abstractmethod


class Host(ABC):
    """
    Abstract class for a host
    The object that gets infected
    """
    def __init__(self):
        """
        The constructor for the host class
        """
        self._infected = False
        self._infectious = False
        self._latencyTime = 0
        self._infectedTime = 0
        self._immune = False

    ##########
    # Properties
    ##########

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

    ##########
    # Property Setters
    ##########

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

    ##########
    # Methods
    ##########

    @abstractmethod
    def increment(self, disease):
        """
        Increments values on the host

        :param disease: The disease class that the model will run for (disease)
        """
        pass

    @abstractmethod
    def decrement(self, disease):
        """
        Decrements values on the host

        :param disease: The disease class that the model will run for (disease)
        """
        pass

