from Wheat_Stem_Rust_Implementation import field
from Framework.Abstract_Classes import container


class Region(container.Container):

    def __init__(self, name):
        super().__init__(name)
        self.species = ""
        self.timestepScale = ""

    def timeStep(self, disease, date):
        # Gets the uninfected host objects
        uninfectedHosts = self.getUninfectedHosts()
        self.calculateDeposition(date, uninfectedHosts)

        for o in self.objects:
            o.timeStep(disease, date)

    def calculateDeposition(self, date, uninfectedHosts):
        for o in self.objects:
            o.calculateDeposition(date, uninfectedHosts, self.species, self.timestepScale)

    def getUninfectedHosts(self):
        """
        Gets the objects of the hosts which are uninfected

        :return: The objects of the uninfected hosts
        """
        uninfectedHosts = []
        for o in self.objects:
            if not o.infected() and not o.immune():
                uninfectedHosts.append(o)
        return uninfectedHosts

    def getInfectedCount(self):
        count = 0
        for o in self.objects:
            count += o.getInfectedCount()

        return count

    def getImmuneCount(self):
        count = 0
        for o in self.objects:
            count += o.getImmuneCount()

        return count

    def increment(self, disease):
        pass

    def decrement(self, disease):
        pass

    def populate(self, db):
        fieldData = db.getFieldData()
        startingSourceList = []
        startingSources = db.getStartingSources()
        for row in startingSources:
            startingSourceList.append(row[0])
        for row in fieldData:
            f = field.Field(row[0], row[1], 0, row[2], row[3], row[4], row[5], row[6])
            f.addHost()
            if f.name in startingSourceList:
                f.infect()
            self.objects.append(f)





