import random
import numberHandler
import person
from Framework import environment, container
import math
import time


class Building(environment.Environment):
    """
    Building class will contain hosts and handle their interactions
    """
    def __init__(self, activePeriod, name, infectionMultiplier, hostObjects):
        """
        Constructor for the building class

        :param activePeriod: List of days that the building will be active (input: string)
        :param name: Name of the building type (string)
        :param infectionMultiplier: A measure of how much the hosts interact with each other (0 - 0.99)
        :param hostObjects: A lists of all the host objects that the building will contain (list)
        """
        super(Building, self).__init__(name, activePeriod, infectionMultiplier)
        # Adds the input host objects to the buildings host population
        self.hosts = hostObjects
        # Converts the input active period into the days it represents
        if activePeriod == "Everyday":
            self.activePeriod = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        elif activePeriod == "Weekdays":
            self.activePeriod = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    def getImmuneCount(self):
        """
        Counts the number of immune hosts in the building
        :return: The number of immune hosts as an int
        """
        # Returns the number of immune hosts
        # count = 0
        # for h in self.hosts:
        #     if h.immune:
        #         count += 1
        return super().getImmuneCount()

    def getInfectedCount(self):
        """
        Counts the number of infected hosts in the building
        :return: The number of infected hosts as an int
        """
        # Returns the number of infected hosts
        # count = 0
        # for h in self.hosts:
        #     if h.infected:
        #         count += 1
        return super().getInfectedCount()

    def timeStep(self, disease, day):
        """
        Simulates a day progressing on the building

        :param disease: The disease the simulation is running
        :param day: The day that is currently being run
        """
        # Runs the calculations to infect new hosts
        # If the building should run given the day
        if day in self.activePeriod:
            # Gets the infected host objects
            infectedHosts = self.getInfectedHosts()
            # If there are infected hosts in the environment
            if len(infectedHosts) != 0:
                # Gets the uninfected host objects
                uninfectedHosts = self.getUninfectedHosts()
                # Foreach infected host
                for _ in infectedHosts:
                    # Calculate their interactions with the other hosts in the building
                    interactions = min(round(numberHandler.generatePoisson(self.infectionMultiplier)), len(uninfectedHosts))
                    # Foreach uninfected host that the infected host has come into contact with
                    for uip in random.sample(uninfectedHosts, interactions):
                        # See if they get infected
                        if random.randint(0, 100) < (disease.infectionChance * 100):
                            uip.infected = True

    def getInfectedHosts(self):
        """
        Gets the objects of the hosts which are infected

        :return: The objects of the infected hosts
        """
        infectedHosts = []
        for h in self.hosts:
            if h.infected:
                infectedHosts.append(h)
        return infectedHosts

    def getUninfectedHosts(self):
        """
        Gets the objects of the hosts which are uninfected

        :return: The objects of the uninfected hosts
        """
        uninfectedHosts = []
        for h in self.hosts:
            if not h.infected and not h.immune:
                uninfectedHosts.append(h)
        return uninfectedHosts

    def increment(self, disease):
        """
        Increment each host

        :param disease: The disease the simulation is running
        """
        for h in self.hosts:
            h.increment(disease)

    def decrement(self, disease):
        """
        Decrement each host

        :param disease: The disease the simulation is running
        """
        for h in self.hosts:
            h.decrement(disease)


class City(container.Container):
    """
    Class which inherits from Container
    Contains environments
    Handle interactions between the buildings
    """
    def __init__(self, name, long, lat, commutePercentage):
        """
        Constructor for the city class

        :param name: Name of the city
        :param long: Longitude of the city
        :param lat: Latitude of the city
        :param commutePercentage: Percentage of the population that will travel to a different city
        """
        super().__init__(name)
        self.longitude = long
        self.latitude = lat
        self.commutePercentage = commutePercentage
        self.commutePopulation = []
        self.hosts = []
        self.shopRange = []

    def populate(self, db):
        """
        Sets up the city

        :param db: The database handler class for accessing the database
        """
        print("Making host objects for {}...".format(self.name))
        # Makes all the hosts that the city will contain
        hostCount = db.getHostCount(self.name)[0]
        for x in range(hostCount):
            self.hosts.append(person.Person())

        print("Made host objects for {}".format(self.name))
        print("Sorting host objects for {}...".format(self.name))

        # Lists used to hold the hosts once they have been sorted out by age
        hostsInEducation = []
        hostsInEmployment = []
        hostsRetired = []

        # Sorts the hosts out by age
        for h in self.hosts:
            if h.age <= 18:
                hostsInEducation.append(h)
            elif h.age > 65:
                hostsRetired.append(h)
            else:
                hostsInEmployment.append(h)

        print("Sorted host objects for {}".format(self.name))
        print("Making environments and adding hosts for {}...".format(self.name))

        # Gets the information about all the environments the city will contain
        environmentInfo = db.getEnvironments(self.name)

        # Makes a copy of the hosts list
        hostObjects = self.hosts.copy()
        # for o in self.objects:
        #     hostObjects += o.hosts

        # TODO: Sort out host objects into a dictionary and then make following code a loop with e[0] as the key
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
        """
        Counts the number of immune hosts objects in each building
        Checks if the building name is "House" so that hosts are not double counted
        :return: The number of immune hosts as an int
        """
        count = 0
        for building in self.objects:
            if building.name == "House":
                count += building.getImmuneCount()
        return count

    def getInfectedCount(self):
        """
        Counts the number of infected hosts objects in each building
        Checks if the building name is "House" so that hosts are not double counted
        :return: the number of infected hosts as an int
        """
        count = 0
        for building in self.objects:
            if building.name == "House":
                count += building.getInfectedCount()
        return count

    def increment(self, disease):
        """
        Runs increment method on each host

        :param disease: The disease that the simulation is running
        """
        for h in self.hosts:
            h.increment(disease)

    def decrement(self, disease):
        """
        Runs decrement method on each host

        :param disease: The disease that the simulation is running
        """
        for h in self.hosts:
            h.decrement(disease)

    def getCommuters(self, percentage):
        """
        Gets the host objects that will travel out of the city for that time step
        :param percentage: The percentage of hosts to take
        :return: The host objects that will travel out of the city
        """
        toReturn = []
        numToReturn = round(len(self.commutePopulation)*percentage)
        for x in range(numToReturn):
            toReturn.append(self.commutePopulation.pop(0))
        return toReturn

    def timeStep(self, disease, day):
        """
        Simulates a day progressing in the city

        :param disease: The disease the simulation is running
        :param day: The name of the day that is being simulated
        """
        # Make a copy of the host objects
        hostObjects = self.hosts.copy()
        for o in self.objects:
            # If the building is a shop (getting the shops population for the day)
            if o.name == "Shop":
                # Find how many hosts will visit this shop
                numToTake = numberHandler.weightedRandom(self.shopRange[0], self.shopRange[1], self.shopRange[2])
                o.hosts = []
                # Randomly take these hosts from the copied host list and append them to the shop
                for _ in range(numToTake):
                    o.hosts.append(hostObjects.pop(random.randint(0, len(hostObjects)-1)))
            # Runs time step on the building
            o.timeStep(disease, day)
        # Updates the commuting population
        # self.commutePopulation = random.sample(self.hosts, round(len(self.hosts)*(self.commutePercentage/100)))
        # Runs the increment and decrement methods on all the buildings in the city
        self.increment(disease)
        self.decrement(disease)


class Country(container.Container):
    """
    A class which inherits from Container
    Will contain cities
    Handles interactions between cities
    Is this framework implementations top level environment
    """
    def __init__(self, name):
        """
        Constructor for the country

        :param name: the name of the country (is left blank because its not used anywhere and doesn't need one)
        """
        super().__init__(name)
        self.percentageMatrix = []
        self.halfwayHouses = []

    # def cityPopulate(self, city, db):
    #     city.populate(db)

    def populate(self, db):
        """
        Sets up the country

        :param db: The database handler class for accessing the database
        """
        # Get the information about the cities contained in the country
        cityDetails = db.getCities()

        print("Retrieved City Information")

        # Makes the cities
        for cityStuff in enumerate(cityDetails):
            self.objects.append(City(cityStuff[1][0], cityStuff[1][1], cityStuff[1][2], cityStuff[1][3]))

        # Populate the cities
        startTime = time.time()
        for city in self.objects:
            city.populate(db)

        # process_list = []
        # for city in self.objects:
        #     p = mp.Process(target=self.cityPopulate, args=[city, db])
        #     p.start()
        #     process_list.append(p)
        #
        # for process in process_list:
        #     process.join()

        print("%s seconds" % (time.time() - startTime))
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
                    # inverts the distance as number of people traveling will be inversely proportional to the distance
                    matrix[counter1][counter2] = 1 / distance

        # Turns the distance into a percentage from each city
        for rowNum, row in enumerate(matrix):
            rowDistance = 0
            for item in row:
                rowDistance += item
            for itemNum, item in enumerate(row):
                self.percentageMatrix[rowNum][itemNum] = item/rowDistance

        print("Made City Matrix")

        # Make halfway houses between cities
        self.halfwayHouses = [[Building("Everyday", "HalfwayHouse", 0.1, []) for x in range(len(cityDetails))] for y in range(len(cityDetails))]

    # def cityTimeStep(self, city):
    #     print(city.name)
    #     city.timeStep(self.disease, self.day)

    def timeStep(self, disease, day):
        """
        Simulates a day progressing in the country
        :param disease: The disease the simulation is running
        :param day: The current day that is being run
        """
        for o in self.objects:
            o.timeStep(disease, day)
        # self.disease = disease
        # self.day = day
        # jobs = Queue()
        # for i in self.objects:
        #     jobs.put(i)
        # # pool = mp.Pool(processes=2)
        # worker = Thread(unwrap_self_cityTimeStep, zip([self] * len(self.objects), self.objects))
        # worker.start()
        #
        # jobs.join()
        #

        # process_list = []
        # for o in self.objects:
        #     p = mp.Process(target=o.timeStep, args=(disease, day))
        #     p.start()
        #     process_list.append(p)
        #
        # for process in process_list:
        #     process.join()

        # 401.8026111125946 Seconds in parallel (100 time steps, two cities, plymouth and exeter)
        # 337.1786530017853 sec not in parallel

        # Populates the halfway houses
        # Halfway houses are used to simulate hosts going between cities and interacting with each other
        for row in range(len(self.halfwayHouses[0])-1):
            for col in range(row+1, len(self.halfwayHouses[0])):
                self.halfwayHouses[row][col].hosts += self.objects[row].getCommuters(self.percentageMatrix[row][col])
                self.halfwayHouses[row][col].hosts += self.objects[col].getCommuters(self.percentageMatrix[col][row])

        # Progresses time on each halfway house
        for row in self.halfwayHouses:
            for h in row:
                h.timeStep(disease, day)
                h.hosts = []

    def getInfectedCount(self):
        """
        Gets the number of infected hosts in the country
        :return: The number of infected hosts as an int
        """
        # count = 0
        # for o in self.objects:
        #     count += o.getInfectedCount()
        return super().getInfectedCount()

    def getImmuneCount(self):
        """
        Gets the number of immune hosts in the country
        :return: The number of immune hosts as an int
        """
        # count = 0
        # for o in self.objects:
        #     count += o.getImmuneCount()
        return super().getImmuneCount()

    def increment(self, disease):
        """
        Calls the increment method on each city

        :param disease: The disease the simulation is running
        """
        # for o in self.objects:
        #     o.increment(disease)
        super().increment(disease)

    def decrement(self, disease):
        """
        Calls the decrement method on each city

        :param disease: The disease the simulation is running
        """
        # for o in self.objects:
        #     o.decrement(disease)
        super().decrement(disease)