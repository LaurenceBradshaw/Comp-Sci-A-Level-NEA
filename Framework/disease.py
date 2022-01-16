from abc import ABC, abstractmethod


class Disease(ABC):

    def __init__(self):
        self._latencyPeriod = 0
        self._infectionChance = 0
        self._duration = 0
        self._immunityProb = 100

    @property
    def latencyPeriod(self):
        return self._latencyPeriod

    @property
    def infectionChance(self):
        return self._infectionChance

    @property
    def duration(self):
        return self._duration

    @property
    def immunityProb(self):
        return self._immunityProb

    @latencyPeriod.setter
    def latencyPeriod(self, value):
        self._latencyPeriod = value

    @infectionChance.setter
    def infectionChance(self, value):
        self._infectionChance = value

    @duration.setter
    def duration(self, value):
        self._duration = value

    @immunityProb.setter
    def immunityProb(self, value):
        self._immunityProb = value
