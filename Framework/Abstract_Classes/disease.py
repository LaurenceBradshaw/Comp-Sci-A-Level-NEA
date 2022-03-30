from abc import ABC, abstractmethod


class Disease(ABC):
    """
    Abstract class for a disease
    """
    def __init__(self):
        """
        Constructor for the disease
        """
        self._latencyPeriod = 0
        self._infectionChance = 0
        self._duration = 0
        self._immuneDuration = 0

    ##########
    # Properties
    ##########

    @property
    def immuneDuration(self):
        return self._immuneDuration

    @property
    def latencyPeriod(self):
        return self._latencyPeriod

    @property
    def infectionChance(self):
        return self._infectionChance

    @property
    def duration(self):
        return self._duration

    ##########
    # Property setters
    #########

    @immuneDuration.setter
    def immuneDuration(self, value):
        self._immuneDuration = value

    @latencyPeriod.setter
    def latencyPeriod(self, value):
        self._latencyPeriod = value

    @infectionChance.setter
    def infectionChance(self, value):
        self._infectionChance = value

    @duration.setter
    def duration(self, value):
        self._duration = value
