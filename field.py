from Framework import environment


class Field(environment.Environment):

    def __init__(self, name, activePeriod, interactionRate, waterType, country, lat, lon, infectiousPeriod):
        super().__init__(name, activePeriod, interactionRate)
        self.waterType = waterType
        self.name = name
        self.country = country
        self.latitude = lat
        self.longitude = lon
        self.infectiousPeriod = infectiousPeriod

    def timeStep(self, disease, day):
        pass

    def getInfectedCount(self):
        pass

    def getImmuneCount(self):
        pass