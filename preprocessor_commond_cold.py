import math
from Framework import preprocessor
import place
import random


class Preprocessing(preprocessor.Preprocessing):
    """
    Class which creates all the other objects for the model
    """
    def __init__(self, db):
        """
        Constructor for the preprocessor

        :param db: The class which handles all actions with the database
        """
        super(Preprocessing, self).__init__()
        self.db = db

    def preprocess(self, disease):
        """
        Runs the preprocessing process

        :param disease: The disease that the simulation with model
        :return: One container type object to the model
        """
        topLevel = place.Country("")
        topLevel.populate(self.db)

        self.initialInfection(disease, topLevel)
        return topLevel

    def initialInfection(self, disease, topLevel):
        try:
            cityNum = random.randint(0, len(topLevel.objects)-1)
            c = topLevel.objects[cityNum]
            buildingNum = random.randint(0, len(c.objects)-1)
            building = c.objects[buildingNum]
            hostNum = random.randint(0, len(building.hosts)-1)
            toInfect = building.hosts[hostNum]
            toInfect.infected = True
            toInfect.infectious = True
            toInfect.infectedTime = 1
            toInfect.latencyTime = disease.latencyPeriod
            print("Initial Infection Location:")
            print("City: {}".format(cityNum))
            print("Building: {}".format(buildingNum))
            print("Host: {}".format(hostNum))
        except ValueError:
            self.initialInfection(disease, topLevel)
