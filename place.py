import random
import functionLib
import person
from Framework import environment, container
import time


class Building(environment.Environment):
    """
    Building class will contain hosts and handle their interactions
    """
    def __init__(self, activePeriod, name, interactionRate, hostObjects):
        """
        Constructor for the building class

        :param activePeriod: List of days that the building will be active (input: string)
        :param name: Name of the building type (string)
        :param interactionRate: A measure of how much the hosts interact with each other (0 - 0.99)
        :param hostObjects: A lists of all the host objects that the building will contain (list)
        """
        super(Building, self).__init__(name, activePeriod, interactionRate)
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
        return super().getImmuneCount()

    def getInfectedCount(self):
        """
        Counts the number of infected hosts in the building
        :return: The number of infected hosts as an int
        """
        return super().getInfectedCount()

    def timeStep(self, disease, day):
        """
        Simulates a day progressing on the building

        :param disease: The disease the simulation is running (disease)
        :param day: The day that is currently being run (string)
        """
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
                    interactions = min(round(functionLib.generatePoisson(self.interactionRate)), len(uninfectedHosts))
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

        :param disease: The disease the simulation is running (disease)
        """
        for h in self.hosts:
            h.increment(disease)

    def decrement(self, disease):
        """
        Decrement each host

        :param disease: The disease the simulation is running (disease)
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

        :param name: Name of the city (string)
        :param long: Longitude of the city (float)
        :param lat: Latitude of the city (float)
        :param commutePercentage: Percentage of the population that will travel to a different city (int)
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
        Makes host and building objects and then run the populate function on them

        :param db: The database handler class for accessing the database (databaseHandler)
        """
        print("Making host objects for {}...".format(self.name))
        # Makes all the hosts that the city will contain
        hostCount = db.getHostCount(self.name)
        for x in range(hostCount):
            self.hosts.append(person.Person())

        print("Made host objects for {}".format(self.name))
        print("Sorting host objects for {}...".format(self.name))

        # Makes a copy of the hosts list
        hostObjects = self.hosts.copy()

        # Dictionary to store hosts sorted by age groups
        peopleByAgeDict = functionLib.sortHosts(self.hosts)

        print("Sorted host objects for {}".format(self.name))
        print("Making environments and adding hosts for {}...".format(self.name))

        # Gets the information about all the environments the city will contain
        environmentInfo = db.getEnvironments(self.name)

        for e in environmentInfo:
            # If the environment is not a shop (with a dynamic population)
            if e[0] != "Shop":
                # For the number of requested environments of that type
                for _ in range(e[1]):
                    # Get the number of people to add to that environment
                    hostCount = functionLib.weightedRandom(e[2], e[3], e[4])
                    hostsToGo = []
                    # Tries to take the required number of hosts
                    try:
                        for _ in range(hostCount):
                            hostsToGo.append(peopleByAgeDict[e[0]].pop(0))
                    # If the list is empty it cant take any so it will catch the error
                    except IndexError:
                        hostsToGo += hostObjects
                    # Makes the environment
                    self.objects.append(Building(e[5], e[0], e[6], hostsToGo))
            else:
                # Adds the range of people that will be going to a shop as an attribute
                self.shopRange += e[2], e[3], e[4]
                # Makes the required number of buildings with an empty population
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

        :param disease: The disease that the simulation is running (disease)
        """
        for h in self.hosts:
            h.increment(disease)

    def decrement(self, disease):
        """
        Runs decrement method on each host

        :param disease: The disease that the simulation is running (disease)
        """
        for h in self.hosts:
            h.decrement(disease)

    def getCommuters(self, percentage):
        """
        Gets the host objects that will travel out of the city for that time step
        :param percentage: The percentage of hosts to take (float)
        :return: The host objects that will travel out of the city (list)
        """
        toReturn = []
        numToReturn = round(len(self.commutePopulation)*percentage)
        for x in range(numToReturn):
            toReturn.append(self.commutePopulation.pop(0))
        return toReturn

    def timeStep(self, disease, day):
        """
        Simulates a day progressing in the city

        :param disease: The disease the simulation is running (disease)
        :param day: The name of the day that is being simulated (string)
        """
        timeStart = time.time()
        # Make a copy of the host objects
        hostObjects = self.hosts.copy()
        # Iterates through each building in the city
        for o in self.objects:
            # If the building is a shop (getting the shops population for the day)
            if o.name == "Shop":
                # Find how many hosts will visit this shop
                numToTake = functionLib.weightedRandom(self.shopRange[0], self.shopRange[1], self.shopRange[2])
                o.hosts = []
                # Randomly take these hosts from the copied host list and append them to the shop
                for _ in range(numToTake):
                    o.hosts.append(hostObjects.pop(random.randint(0, len(hostObjects)-1)))
            # Runs time step on the building
            o.timeStep(disease, day)
        # Updates the commuting population
        self.commutePopulation = random.sample(self.hosts, round(len(self.hosts)*(self.commutePercentage/100)))
        # Runs the increment and decrement methods on all the buildings in the city
        self.increment(disease)
        self.decrement(disease)
        print(self.name+": %s seconds" % (time.time() - timeStart))


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

        :param name: the name of the country (is left blank because its not used anywhere and doesn't need one) (string)
        """
        super().__init__(name)
        self.percentageMatrix = []
        self.halfwayHouses = []

    def populate(self, db):
        """
        Sets up the country

        :param db: The database handler class for accessing the database (databaseHandler)
        """
        # Get the information about the cities contained in the country
        cityDetails = db.getCities()

        print("Retrieved City Information")

        for i in range(len(cityDetails['CityID'])):
            self.objects.append(functionLib.makeCity(cityDetails['CityID'][i], cityDetails['Longitude'][i], cityDetails['Latitude'][0], cityDetails['CommutePercentage'][0]))
        # Makes the cities
        # for cityStuff in cityDetails:
        #    self.objects.append(makeCity(cityStuff))

        # Populate the cities
        startTime = time.time()
        for city in self.objects:
            city.populate(db)

        print("%s seconds" % (time.time() - startTime))
        print("Finished All Cities")
        print("Making City Matrix...")

        self.percentageMatrix = functionLib.makeMatrix(cityDetails)

        print("Made City Matrix")

        # Make halfway houses between cities
        self.halfwayHouses = functionLib.makeHalfwayHouses(cityDetails)

    def timeStep(self, disease, day):
        """
        Simulates a day progressing in the country
        :param disease: The disease the simulation is running (disease)
        :param day: The current day that is being run (string)
        """
        for o in self.objects:
            o.timeStep(disease, day)

        # Populates the halfway houses
        # Halfway houses are used to simulate hosts going between cities and interacting with each other
        # Only does half the matrix
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
        return super().getInfectedCount()

    def getImmuneCount(self):
        """
        Gets the number of immune hosts in the country
        :return: The number of immune hosts as an int
        """
        return super().getImmuneCount()

    def increment(self, disease):
        """
        Calls the increment method on each city

        :param disease: The disease the simulation is running (disease)
        """
        super().increment(disease)

    def decrement(self, disease):
        """
        Calls the decrement method on each city

        :param disease: The disease the simulation is running (disease)
        """
        super().decrement(disease)



