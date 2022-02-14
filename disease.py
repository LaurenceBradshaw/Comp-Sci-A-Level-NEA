from Framework import disease


class Disease(disease.Disease):
    """
    Class for the disease
    """
    def __init__(self, diseaseDetails):
        """
        Constructor for the disease class

        :param diseaseDetails: Info from the database for the disease (pyodbc row)
        """
        super(Disease, self).__init__()
        self.latencyPeriod = diseaseDetails[1]
        self.infectionChance = diseaseDetails[2]
        self.duration = diseaseDetails[0]
        self.immuneDuration = diseaseDetails[3]

