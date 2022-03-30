import math
import random
from numpy import random as rn
import place
import person
from Framework import validation


def generatePoisson(rate):
    # Checking the rate is within the expected range
    validation.generatePoissonRange(rate)

    res = random.randint(0, 100)/101.0
    a = -math.log(1.0-res)/(1-rate)

    return a


def weightedRandom(lb, ub, avg):
    # Checking the average is within the lower and upper bounds
    validation.weightedRandomRange(lb, ub, avg)

    x = []
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
    validation.coordRange(lon1)
    validation.coordRange(lon2)
    validation.coordRange(lat1)
    validation.coordRange(lat2)

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
    validation.isFloat(lon)
    validation.isFloat(lat)
    validation.isString(ID)
    validation.isNoneNegativeInt(commutePercentage)
    validation.percentageRange(commutePercentage)
    return place.City(ID, lon, lat, commutePercentage)


def makeBuilding(activePeriod, name, interactionRate, hosts):
    validation.isString(activePeriod)
    validation.knownActivePeriod(activePeriod)
    validation.isString(name)
    validation.isNoneNegativeFloat(interactionRate)
    validation.isList(hosts)
    if len(hosts) != 0:
        validation.isHost(hosts[0])
    return place.Building(activePeriod, name, interactionRate, hosts)


def sortHosts(hosts):
    peopleByAgeDict = {
        "House": hosts,
        "Office": [],
        "School": [],
    }

    # Sorts the hosts out by age
    for h in hosts:
        # If a child
        if h.age <= 18:
            peopleByAgeDict["School"].append(h)
        # If not a child and of working age
        elif 18 < h.age <= 65:
            peopleByAgeDict["Office"].append(h)

    return peopleByAgeDict


def selectCount(count, items):
    toGo = []
    # Tries to take the required number of hosts
    try:
        for _ in range(count):
            toGo.append(items.pop(random.randint(0, len(items)-1)))
    # If the list is empty it cant generate a random number so it will catch the error
    except ValueError:
        toGo += items

    return toGo


def makeHosts(count):
    hosts = []
    for _ in range(count):
        hosts.append(person.Person())

    return hosts
