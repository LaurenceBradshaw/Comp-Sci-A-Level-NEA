from Wheat_Stem_Rust_Implementation import field
from Framework.Abstract_Classes import container


class Region(container.Container):

    def __init__(self, name):
        super().__init__(name)
        self.maxDeposition = 0
        self.species = ""
        self.timestepScale = ""
        self.probabilityThreshold = 0

    def timeStep(self, disease, date):

        # Gets the uninfected host objects
        uninfectedHosts = self.getUninfectedHosts()
        for o in self.objects:
            o.timeStep(disease, date, uninfectedHosts, self.maxDeposition, self.species, self.timestepScale, self.probabilityThreshold)

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
        pass

    def getImmuneCount(self):
        pass

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
            f = field.Field(row[0], row[5], 0, row[4], row[1], row[2], row[3], row[6])
            f.addHost()
            if f.name in startingSourceList:
                f.infect()
            self.objects.append(f)





