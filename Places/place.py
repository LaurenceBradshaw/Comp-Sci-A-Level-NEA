import random
import container
import numberHandler
import person
from Framework import environment, host
import math


class Building(environment.Environment):
    # Building class will contain hosts and handle their interactions
    def __init__(self, activePeriod, name, infectionMultiplier, hostObjects):
        super(Building, self).__init__(name, activePeriod, infectionMultiplier)
        self.populate(hostObjects)
        if activePeriod == "Everyday":
            self.activePeriod = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        elif activePeriod == "Weekdays":
            self.activePeriod = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    def populate(self, hostObjects):
        for p in hostObjects:
            self.hosts.append(p)

    def getImmuneCount(self):
        # Returns the number of immune hosts
        count = 0
        for h in self.hosts:
            if h.immune:
                count += 1
        return count

    def getInfectedCount(self):
        # Returns the number of infected hosts
        count = 0
        for h in self.hosts:
            if h.infected:
                count += 1
        return count

    def timeStep(self, disease, day):
        # Runs the calculations to infect new hosts
        if day in self.activePeriod:
            infectedHosts = self.getInfectedHosts()
            uninfectedHosts = self.getUninfectedHosts()

            if len(infectedHosts) != 0:
                for _ in infectedHosts:
                    interactions = min(round(numberHandler.generatePoisson(self.infectionMultiplier)), len(uninfectedHosts))
                    for uip in random.sample(uninfectedHosts, interactions):
                        if random.randint(0, 100) < (disease.infectionChance * 100):
                            uip.infected = True

    def getInfectedHosts(self):
        # Returns the infected host objects
        infectedHosts = []
        for h in self.hosts:
            if h.infected:
                infectedHosts.append(h)
        return infectedHosts

    def getUninfectedHosts(self):
        # Returns the uninfected host objects that can be infected
        uninfectedHosts = []
        for h in self.hosts:
            if not h.infected and not h.immune:
                uninfectedHosts.append(h)
        return uninfectedHosts

    def increment(self, disease):
        for h in self.hosts:
            h.increment(disease)

    def decrement(self, disease):
        for h in self.hosts:
            h.decrement(disease)


class City(container.Container):
    # City will contain and interact between the buildings

    def __init__(self, name, long, lat, commutePercentage):
        super().__init__(name)
        self.longitude = long
        self.latitude = lat
        self.commutePercentage = commutePercentage
        self.commutePopulation = []
        self.hosts = []
        self.shopRange = []

    def populate(self, db):
        # Makes all the environments the city contains
        print("Making host objects for {}...".format(self.name))
        # Makes host classes for the city
        hostCount = db.getHostCount(self.name)[0]
        for x in range(hostCount):
            self.hosts.append(person.Person())

        print("Made host objects for {}".format(self.name))
        print("Sorting host objects for {}...".format(self.name))

        hostsInEducation = []
        hostsInEmployment = []
        hostsRetired = []

        for h in self.hosts:
            if h.age <= 18:
                hostsInEducation.append(h)
            elif h.age > 65:
                hostsRetired.append(h)
            else:
                hostsInEmployment.append(h)

        print("Sorted host objects for {}".format(self.name))
        print("Making environments and adding hosts for {}...".format(self.name))

        environmentInfo = db.getEnvironments(self.name)

        hostObjects = self.hosts.copy()
        # for o in self.objects:
        #     hostObjects += o.hosts

        for e in environmentInfo:
            if e[0] == "House":
                for x in range(e[1]):
                    hostCount = numberHandler.weightedRandom(e[2], e[3], e[4])
                    hostsToGo = []
                    try:
                        for _ in range(hostCount):
                            hostsToGo.append(hostObjects.pop(0))
                    except IndexError:
                        hostsToGo += hostObjects
                    self.objects.append(Building(e[5], e[0], e[6], hostsToGo))
            elif e[0] == "Office":
                for x in range(e[1]):
                    hostCount = numberHandler.weightedRandom(e[2], e[3], e[4])
                    hostsToGo = []
                    try:
                        for _ in range(hostCount):
                            hostsToGo.append(hostsInEmployment.pop(0))
                    except IndexError:
                        hostsToGo += hostsInEmployment
                    self.objects.append(Building(e[5], e[0], e[6], hostsToGo))
            elif e[0] == "School":
                for x in range(e[1]):
                    hostCount = numberHandler.weightedRandom(e[2], e[3], e[4])
                    hostsToGo = []
                    try:
                        for _ in range(hostCount):
                            hostsToGo.append(hostsInEducation.pop(0))
                    except IndexError:
                        hostsToGo += hostsInEducation
                    self.objects.append(Building(e[5], e[0], e[6], hostsToGo))
            elif e[0] == "Shop":
                self.shopRange += e[2], e[3], e[4]
                for x in range(e[1]):
                    self.objects.append(Building(e[5], e[0], e[6], []))

        print("Made environments and added hosts for {}".format(self.name))
        print("Finished {}".format(self.name))

    def getImmuneCount(self):
        count = 0
        for building in self.objects:
            if building.name == "House":
                count += building.getImmuneCount()

        return count

    def getInfectedCount(self):
        count = 0
        for building in self.objects:
            if building.name == "House":
                count += building.getInfectedCount()

        return count

    def increment(self, disease):
        for o in self.objects:
            if o.name == "House":
                for h in o.hosts:
                    h.increment(disease)

    def decrement(self, disease):
        for o in self.objects:
            if o.name == "House":
                for h in o.hosts:
                    h.decrement(disease)

    def getCommuters(self, percentage):
        toReturn = []
        numToReturn = round(len(self.commutePopulation)*percentage)
        for x in range(numToReturn):
            toReturn.append(self.commutePopulation.pop(0))
        return toReturn

    def timeStep(self, disease, day):
        hostObjects = self.hosts.copy()
        for o in self.objects:
            if o.name == "Shop":
                numToTake = numberHandler.weightedRandom(self.shopRange[0], self.shopRange[1], self.shopRange[2])
                o.hosts = []
                random.shuffle(o.hosts)
                for _ in range(numToTake):
                    o.hosts.append(hostObjects.pop(0))
            o.timeStep(disease, day)
        self.commutePopulation = random.sample(self.hosts, round(len(self.hosts)*(self.commutePercentage/100)))
        self.increment(disease)
        self.decrement(disease)


class Country(container.Container):
    # Country will contain and interact between cities
    def __init__(self, name):
        super().__init__(name)
        self.percentageMatrix = []
        self.halfwayHouses = []

    def populate(self, db):
        cityDetails = db.getCities()

        print("Retrieved City Information")

        for cityStuff in enumerate(cityDetails):
            self.objects.append(City(cityStuff[1][0], cityStuff[1][1], cityStuff[1][2], cityStuff[1][3]))

        for city in self.objects:
            city.populate(db)

        print("Finished All Cities")
        print("Making City Matrix...")

        # Matrix that stores the distances between the cities
        matrix = [[0.0 for x in range(len(cityDetails))] for y in range(len(cityDetails))]
        # the percentage (in decimal) that the number of people going to that city will be out of all the selected people to travel between cities
        self.percentageMatrix = [[0.0 for x in range(len(cityDetails))] for y in range(len(cityDetails))]
        for counter1, city1 in enumerate(cityDetails):
            for counter2, city2 in enumerate(cityDetails):
                if city1[0] != city2[0]:
                    distance = math.sqrt(math.pow(city1[1] - city2[1], 2) + math.pow(city1[2] - city2[2], 2))
                    matrix[counter1][counter2] = 1 / distance  # inverts the distance as number of people traveling will be inversely proportional to the distance

        for rowNum, row in enumerate(matrix):
            rowDistance = 0
            for item in row:
                rowDistance += item
            for itemNum, item in enumerate(row):
                self.percentageMatrix[rowNum][itemNum] = item/rowDistance

        print("Made City Matrix")

        # make halfway houses
        halfwayCount = (math.pow(len(self.objects)-1, 2) - len(self.objects)-1)/2  # Triangle numbers
        # TODO make list of used combination indexes?
        self.halfwayHouses = [[Building("Everyday", "HalfwayHouse", 0.5, []) for x in range(len(cityDetails))] for y in range(len(cityDetails))]
        usedIndexes = []
        # TODO Make cities return the people to add to the halfway house

        # Pog 07/01/2022
        # totalDistance = 0  # sum of all the inverse distances between cities
        # for row in matrix:
        #     for item in row:
        #         totalDistance += item
        #
        # rowCounter = 0
        # for row in matrix:
        #     itemCounter = 0
        #     for item in row:
        #         self.percentageMatrix[rowCounter][itemCounter] = (item / totalDistance)
        #         itemCounter += 1
        #     rowCounter += 1

    def timeStep(self, disease, day):
        for o in self.objects:
            o.timeStep(disease, day)

        for row in range(len(self.halfwayHouses[0])-1):
            for col in range(row+1, len(self.halfwayHouses[0])):
                self.halfwayHouses[row][col].hosts += self.objects[row].getCommuters(self.percentageMatrix[row][col])
                self.halfwayHouses[row][col].hosts += self.objects[col].getCommuters(self.percentageMatrix[col][row])

        # for cityFrom, row in enumerate(self.halfwayHouses):
        #     for cityTo, halfwayHouse in enumerate(row):
        #         if len(self.halfwayHouses[cityTo][cityFrom].hosts) == 0:
        #             halfwayHouse.hosts += self.objects[cityFrom].getCommuters(self.percentageMatrix[cityFrom][cityTo])

        for row in self.halfwayHouses:
            for h in row:
                h.timeStep(disease, day)
                h.hosts = []

    def getImmuneCount(self):
        count = 0
        for city in self.objects:
            count += city.getImmuneCount()

        return count

    def getInfectedCount(self):
        count = 0
        for city in self.objects:
            count += city.getInfectedCount()

        return count

# class Place(environment.Environment):

    # def __init__(self, name, lb, ub, activePeriod, infectionMultiplier):
    #     super(Place, self).__init__(name, self.convertActivePeriod(activePeriod), infectionMultiplier)
    #     self.lowerBound = lb
    #     self.upperBound = ub
    #
    # def convertActivePeriod(self, activePeriod):
    #     if activePeriod == "Everyday":
    #         return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #     elif activePeriod == "Weekdays":
    #         return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #
    # def populate(self, people, avg):
    #     return self.people.populate(people, self.lowerBound, self.upperBound, avg)
    #
    # def timeStep(self, disease):
    #     uninfectedPeopleList = self.people.getUninfectedPeople()
    #     infectedPeopleList = self.people.getInfectedPeople()
    #
    #     if len(infectedPeopleList) != 0:
    #         for _ in infectedPeopleList:
    #             interactions = min(round(numberHandler.generatePoisson(self.infectionMultiplier)), len(uninfectedPeopleList))
    #             for uip in random.sample(uninfectedPeopleList, interactions):
    #                 if random.randint(0, 100) < (disease.infectionChance * 100):
    #                     uip.infected = True

        # gets the number of people to infect
#        numToInfect = min(round(numberHandler.generatePoisson(self.infectionMultiplier)), len(uninfectedPeopleList))

#        # calculates the probability of there being an infection in the place
#        probability = 0
#        for _ in infectedPeopleList:
#            probability += disease.infectionChance

#        # if the probability is hit then people are infected
#        if random.randint(0, 100) < probability * 100 and numToInfect > 0:
#            peopleToInfect = random.sample(uninfectedPeopleList, numToInfect)
#            for personToInfect in peopleToInfect:
#                personToInfect.infected = True
