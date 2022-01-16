import math
from Places import city


class Country(object):

    def __init__(self, cityDetails):
        self.cities = []

        counter1 = 0
        counter2 = 0
        # Matrix that stores the distances between the cities
        self.matrix = [[0.0 for x in range(len(cityDetails))] for y in range(len(cityDetails))]
        # the percentage (in decimal) that the number of people going to that city will be out of all the selected people to travel between cities
        self.percentageMatrix = [[0.0 for x in range(len(cityDetails))] for y in range(len(cityDetails))]
        for city1 in cityDetails:
            for city2 in cityDetails:
                if city1[0] != city2[0]:
                    distance = math.sqrt(math.pow(city1[1] - city2[1], 2) + math.pow(city1[2] - city2[2], 2))
                    self.matrix[counter1][counter2] = 1/distance  # inverts the distance as number of people traveling will be inversely proportional to the distance
                counter2 += 1
            counter2 = 0
            counter1 += 1

        totalDistance = 0  # sum of all the inverse distances between cities
        for row in self.matrix:
            for item in row:
                totalDistance += item

        rowCounter = 0
        for row in self.matrix:
            itemCounter = 0
            for item in row:
                self.percentageMatrix[rowCounter][itemCounter] = (item/totalDistance)
                itemCounter += 1
            rowCounter += 1

        # Make Cities
        placeInMatrix = 0  # used to indicate the cities place in the matrix
        for cityInfo in cityDetails:
            self.cities.append(city.City(cityInfo[0], cityInfo[1], cityInfo[2], placeInMatrix, cityInfo[3]))  # City name, longitude, latitude, index in matrix array
            placeInMatrix += 1

    def timeStep(self, disease, day):
        for city in self.cities:
            city.timeStep(disease, day)

    def getInfectedCount(self):
        infectedCount = 0
        for city in self.cities:
            for person in city.hosts:
                if person.infected:
                    infectedCount += 1
        return infectedCount

    def getImmuneCount(self):
        immuneCount = 0
        for city in self.cities:
            for person in city.hosts:
                if person.immune:
                    immuneCount += 1
        return immuneCount
