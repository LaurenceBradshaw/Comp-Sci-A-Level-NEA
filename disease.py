from Framework import disease


class Disease(disease.Disease):

    def __init__(self, diseaseDetails):
        super(Disease, self).__init__()
        self.latencyPeriod = diseaseDetails[1]
        self.infectionChance = diseaseDetails[2]
        self.duration = diseaseDetails[0]
        self.immunityProb = diseaseDetails[3]
        self.immuneDuration = diseaseDetails[4]

