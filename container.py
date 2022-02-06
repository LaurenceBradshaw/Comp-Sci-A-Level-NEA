from abc import ABC, abstractmethod

# Objects that count as a container:
# - City (contains environments)
# - Country (contains cities)

# Preprocessing must return one container to the main model script
# TODO Make abstract


class Container(ABC):

    def __init__(self, name):
        self._objects = []
        self._name = name

    @property
    def objects(self):
        return self._objects

    @property
    def name(self):
        return self._name

    @objects.setter
    def objects(self, value):
        self._objects = value

    @abstractmethod
    def timeStep(self, disease, day):
        for o in self.objects:
            o.timeStep(disease, day)

    @abstractmethod
    def getInfectedCount(self):
        count = 0
        for o in self.objects:
            count += o.getInfectedCount()
        return count

    @abstractmethod
    def getImmuneCount(self):
        count = 0
        for o in self.objects:
            count += o.getImmuneCount()
        return count

    @abstractmethod
    def increment(self, disease):
        for o in self.objects:
            o.increment(disease)

    @abstractmethod
    def decrement(self, disease):
        for o in self.objects:
            o.decrement(disease)

    @abstractmethod
    def populate(self, db):
        pass
