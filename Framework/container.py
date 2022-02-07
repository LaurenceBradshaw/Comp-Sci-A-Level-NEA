from abc import ABC, abstractmethod


class Container(ABC):
    """
    Abstract class for containers
    A container is used for holding objects
    Examples:
        City (contains environments)
        Country (contains cities)

    The preprocessing must return one top level container (not contained by anything itself)
    """

    def __init__(self, name):
        self._objects = []
        self._name = name

    ##########
    # Properties
    ##########

    @property
    def objects(self):
        return self._objects

    @property
    def name(self):
        return self._name

    ##########
    # Property setters
    ##########

    @objects.setter
    def objects(self, value):
        self._objects = value

    @name.setter
    def name(self, value):
        self._name = value

    ##########
    # Methods
    ##########

    @abstractmethod
    def timeStep(self, disease, day):
        """
        Simulates a day on each object in the container

        :param disease: The disease that is running in the simulation
        :param day: That name of the day that is being run
        """
        for o in self.objects:
            o.timeStep(disease, day)

    @abstractmethod
    def getInfectedCount(self):
        """
        Gets the number of infected hosts from all the objects in the container

        :return: The number of infected hosts as an int
        """
        count = 0
        for o in self.objects:
            count += o.getInfectedCount()
        return count

    @abstractmethod
    def getImmuneCount(self):
        """
        Gets the number of immune ghosts from all the objects in the container

        :return: The number of infected hosts as an int
        """
        count = 0
        for o in self.objects:
            count += o.getImmuneCount()
        return count

    @abstractmethod
    def increment(self, disease):
        """
        Tells the contained objects to increment time
        Incrementing time increases the counter on a host

        :param disease: The disease that the simulation is running
        """
        for o in self.objects:
            o.increment(disease)

    @abstractmethod
    def decrement(self, disease):
        """
        Tells the contained objects to decrement time
        Decrementing time checks if a hosts has been infected for the disease duration and makes them not infected if so

        :param disease: The disease that the simulation is running
        """
        for o in self.objects:
            o.decrement(disease)

    @abstractmethod
    def populate(self, db):
        """
        Will populate the container with objects

        :param db: The database handler class for accessing the database
        """
        pass
