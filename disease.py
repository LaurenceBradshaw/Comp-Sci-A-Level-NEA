from Framework import disease


class Disease(disease.Disease):

    def __init__(self):
        super(Disease, self).__init__()
        self.latencyPeriod = 2
        self.infectionChance = 0.1
        self.duration = 14
        self.immunityProb = 100
        # TODO populate this from the database
