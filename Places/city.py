import random


class City(object):

    def __init__(self, name, long, lat, number, percentage):
        self.places = []
        self.name = name
        self.longitude = long
        self.latitude = lat
        self.hosts = []
        self.shopCount = 0
        self.number = number
        self.commutePercentage = percentage
        self.commuters = []

    def increment(self, disease):  # increments the values on the hosts if required
        for e in self.places:
            for p in e.people.list:
                p.increment(disease)

    def decrement(self, disease):  # decreases the values on the hosts if required
        for e in self.places:
            for p in e.people.list:
                p.decrement(disease)

    def getImmune(self):  # Counts the number of immune hosts in the city
        immuneCount = 0
        for environment in self.places:
            if environment.name == "House":
                for person in environment.people.list:
                    if person.immune:
                        immuneCount += 1
        return immuneCount

    def getInfected(self):  # Counts the number of infected hosts in the city
        infectedCount = 0
        for environment in self.places:
            if environment.name == "House":
                for person in environment.people.list:
                    if person.infected:
                        infectedCount += 1
        return infectedCount

    def timeStep(self, disease, day):  # Progresses time on the city
        hosts = self.hosts.copy()
        self.commuters = random.sample(self.hosts, round(len(self.hosts)*(self.commutePercentage/100)))

        shopsFilled = 0
        for p in self.places:
            if p.name == "Shop":
                hosts = p.populate(hosts, abs(len(hosts)/(self.shopCount - shopsFilled + 1)))
                shopsFilled += 1
                if day in p.activePeriod:
                    p.timeStep(disease)

    def populate(self, people):  # populates the city and assigns people to environments
        peopleInEducation = []
        peopleInEmployment = []
        peopleRetired = []
        peopleInHouses = people.copy()
        self.hosts = people.copy()
        houseCount = 0
        officeCount = 0
        schoolCount = 0

        for environment in self.places:
            if environment.name == "House":
                houseCount += 1

        for environment in self.places:
            if environment.name == "Office":
                officeCount += 1

        for environment in self.places:
            if environment.name == "School":
                schoolCount += 1

        for environment in self.places:
            if environment.name == "Shop":
                self.shopCount += 1

        for p in people:
            # p.age = numberHandler.weightedRandom(1, 100, 35)
            if p.age <= 18:
                peopleInEducation.append(p)
            elif p.age > 65:
                peopleRetired.append(p)
            else:
                peopleInEmployment.append(p)

        housesFilled = 0
        schoolsFilled = 0
        officesFilled = 0
        for p in self.places:
            if p.name == "House":
                peopleInHouses = p.populate(peopleInHouses, len(peopleInHouses)/(houseCount-housesFilled+1))
                housesFilled += 1
            elif p.name == "School":
                peopleInEducation = p.populate(peopleInEducation, abs(len(peopleInEducation)/(schoolCount-schoolsFilled+1)))
                schoolsFilled += 1
            elif p.name == "Office":
                peopleInEmployment = p.populate(peopleInEmployment, abs(len(peopleInEmployment)/(officeCount-officesFilled+1)))
                officesFilled += 1

        print("City Done")
