import random
import numberHandler
from Framework import host


class Person(host.Host):

    def __init__(self):
        self.age = numberHandler.weightedRandom(1, 100, 35)
        super(Person, self).__init__()
        self.immuneDuration = 0

    def getAge(self):
        return self.age

    def increment(self, disease):
        # increases time infected on people infected
        if self.infected and not self.immune:
            print(self.infectedTime)
            self.latencyTime += 1
            self.infectedTime += 1
        if self.latencyTime >= disease.latencyPeriod:
            self.infectious = True
        if self.immune:
            self.immuneDuration += 1

    def decrement(self, disease):
        # removes infected status from people who have been infected for the disease duration
        if self.infectedTime >= disease.duration:
            self.infected = False
            self.infectious = False
            self.latencyTime = 0
            self.infectedTime = 0
            # probability of becoming immune after having the disease
            x = random.randint(0, 100)
            if x < disease.immunityProb:
                self.immune = True

        if self.immuneDuration >= disease.immuneDuration:
            self.immune = False
            self.immuneDuration = 0
