from Framework.Abstract_Classes import preprocessor
from Wheat_Stem_Rust_Implementation import east_africa_middle_east


class Preprocessing(preprocessor.Preprocessing):

    def __init__(self, db):
        super(Preprocessing, self).__init__()
        self.db = db

    def preprocess(self, disease):
        region = east_africa_middle_east.Region('')
        region.populate(self.db)
        simulationParameters = self.db.getSimulationParameters()
        disease.maxDeposition = simulationParameters[0]
        disease.probabilityThreshold = simulationParameters[1]
        region.species = simulationParameters[2]
        region.timestepScale = simulationParameters[3]

        return region

    def initialInfection(self, disease, topLevel):
        pass

