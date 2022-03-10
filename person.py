import functionLib
from Framework import host


class Person(host.Host):
    """
    Class for the host of the model
    """
    def __init__(self):
        """
        Constructor for the host class
        """
        self.age = functionLib.weightedRandom(1, 100, 35)
        super(Person, self).__init__()

    def getAge(self):
        """
        Gets the age of the person

        :return: The age property of the host (int)
        """
        return self.age

    def increment(self, disease):
        """
        Increments the time a person is infected for if applicable

        :param disease: The disease the simulation is running (disease)
        """
        # Increases time infected on people infected if they are infected
        if self.infected and not self.immune:
            self.latencyTime += 1
            self.infectedTime += 1
        # Checks if they have been infected for the duration of the disease
        if self.latencyTime >= disease.latencyPeriod:
            self.infectious = True
        # Increments the amount of time a person has been immune for
        if self.immune:
            self.immuneTime += 1

    def decrement(self, disease):
        """
        Removes the infected status from a person if they have been infected for the disease duration

        :param disease: The disease the simulation is running (disease)
        """
        # Removes infected status from people who have been infected for the disease duration
        if self.infectedTime >= disease.duration:
            self.infected = False
            self.infectious = False
            self.latencyTime = 0
            self.infectedTime = 0
            self.immune = True
        # Removes immune status from people who have been immune for the disease immunity period
        if self.immuneTime >= disease.immuneDuration:
            self.immune = False
            self.immuneTime = 0
