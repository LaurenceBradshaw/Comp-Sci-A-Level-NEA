import math
from Framework import preprocessor
import person
from Places import city
from Places import place
import random
import country


class Preprocessing(preprocessor.Preprocessing):

    def __init__(self, db):
        super(Preprocessing, self).__init__()
        self.db = db

    def preprocess(self, disease):

        topLevel = place.Country("")
        topLevel.populate(self.db)

        # cities = []  # list for all the cities to return from the preprocessor
        # cityDetails = self.db.getCities()  # returns a list of rows from the database where each row contains the city name, long and then lat
        #
        # topLevel = country.Country(cityDetails)
        #
        # # Add environments to each city in the country
        # for c in topLevel.cities:
        #     environments = self.db.getEnvironments(c.name)
        #     for e in environments:
        #         for x in range(e[1]):
        #             c.places.append(place.Place(e[0], e[2], e[3], e[4], e[5]))  # Name, lowerbound, upperbound, activePeriod, infectionMultiplier
        # # Make and add hosts to each city in the country
        # for c in topLevel.cities:
        #     hostCount = self.db.getHostCount(c.name)[0]  # returns the number of hosts the city 'c' should have
        #     hosts = []  # list to hold city hosts before adding them to the city object
        #     for x in range(hostCount):
        #         hosts.append(person.Person())
        #     c.populate(hosts)  # adds newly made hosts to the city

        # # Make Cities
        # placeInMatrix = 0  # used to indicate the cities place in the matrix
        # for cityInfo in cityDetails:
        #     cities.append(city.City(cityInfo[0], cityInfo[1], cityInfo[2], placeInMatrix, cityInfo[3]))  # City name, longitude, latitude, index in matrix array
        #     placeInMatrix += 1
        # # Add environments to each city
        # for c in countries.cities:
        #     environments = self.db.getEnvironments(c.name)
        #     for e in environments:
        #         for x in range(e[1]):
        #             c.places.append(place.Place(e[0], e[2], e[3], e[4], e[5]))  # Name, lowerbound, upperbound, activePeriod, infectionMultiplier
        # # Make and add hosts to each city
        # for c in cities:
        #     hostCount = self.db.getHostCount(c.name)[0]  # returns the number of hosts the city 'c' should have
        #     hosts = []  # list to hold city hosts before adding them to the city object
        #     for x in range(hostCount):
        #         hosts.append(person.Person())
        #     c.populate(hosts)  # adds newly made hosts to the city
        # # Creates an adjacency matrix with the distances of each city to each other
        # matrix = self.makeMatrix(cityDetails)
        # # Gives each city the part of the matrix that it needs (could be static to the city class?)
        # counter = 0
        # for c in cities:
        #     c.matrix = matrix[counter]
        #     counter += 1
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
        except IndexError:
            self.initialInfection(disease, topLevel)

    def makeMatrix(self, cityInfo):
        counter1 = 0
        counter2 = 0
        matrix = [[0.0 for x in range(len(cityInfo))] for y in range(len(cityInfo))]
        for city1 in cityInfo:
            for city2 in cityInfo:
                if city1[0] != city2[0]:
                    distance = math.sqrt(math.pow(city1[1]-city2[1], 2) + math.pow(city1[2]-city2[2], 2))
                    matrix[counter1][counter2] = distance
                counter2 += 1
            counter2 = 0
            counter1 += 1

        return matrix
