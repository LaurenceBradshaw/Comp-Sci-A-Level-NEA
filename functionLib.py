import math
import random
from numpy import random as rn
import place


class RateOutOfRange(Exception):
    pass


def generatePoisson(rate):
    if 0 < rate < 1:
        res = random.randint(0, 100)/101.0

        a = -math.log(1.0-res)/(1-rate)
    else:
        raise RateOutOfRange('Interaction Rate Is Out Of The Expected Range')

    return a


def weightedRandom(lb, ub, avg):
    x = []
    # Checking if the average is the same as the bounds
    avg = ub if ub-avg < 0 else avg
    avg = lb if avg-lb < 0 else avg
    valid = False
    while not valid:
        if avg - lb > ub - avg:
            x = rn.normal(loc=avg, scale=(ub - avg) / 2, size=1)
        else:
            x = rn.normal(loc=avg, scale=(avg - lb) / 2, size=1)
        if lb <= x[0] <= ub:
            valid = True
    return round(x[0])


def coordsToDistance(lon1, lon2, lat1, lat2):
    # R = 3959.87433 for distance in miles.  For Earth radius in kilometers use 6372.8 km
    R = 6372.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def makeMatrix(cityDetails):
    # Matrix that stores the distances between the cities
    matrix = [[0.0 for x in range(len(cityDetails['CityID']))] for y in range(len(cityDetails['CityID']))]
    # the percentage (in decimal) that the number of people going to that city will be out of all the selected people to travel between cities
    percentageMatrix = matrix.copy()
    for i in range(len(cityDetails['CityID'])):
        for j in range(len(cityDetails['CityID'])):
            if cityDetails['CityID'][i] != cityDetails['CityID'][j]:
                distance = coordsToDistance(cityDetails['Longitude'][i], cityDetails['Longitude'][j], cityDetails['Latitude'][i], cityDetails['Latitude'][j])
                # inverts the distance as number of people traveling will be inversely proportional to the distance
                # removes distances longer than 250km to simulate a typical journey length
                if distance < 250:
                    matrix[i][j] = 1 / distance
                else:
                    matrix[i][j] = 0.0

    # Turns the distance into a percentage from each city
    for rowNum, row in enumerate(matrix):
        # Finds the total amount of distance that each row has
        rowDistance = 0
        for item in row:
            rowDistance += item
        if rowDistance == 0:
            raise ZeroDivisionError('At least one city is too far from any other city to send hosts between')
        # Turns each distance into a percentage
        for itemNum, item in enumerate(row):
            percentageMatrix[rowNum][itemNum] = item / rowDistance

    return percentageMatrix


def makeHalfwayHouses(cityDetails):
    return [[place.Building("Everyday", "HalfwayHouse", 0.1, []) for x in range(len(cityDetails['CityID']))] for y in range(len(cityDetails['CityID']))]


def makeCity(ID, lon, lat, commutePercentage):
    return place.City(ID, lon, lat, commutePercentage)


