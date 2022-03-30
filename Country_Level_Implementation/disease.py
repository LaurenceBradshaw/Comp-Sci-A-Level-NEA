from Framework.Abstract_Classes import disease


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
        self.latencyPeriod = diseaseDetails['LatencyPeriod']
        self.infectionChance = diseaseDetails['InfectionChance']
        self.duration = diseaseDetails['Duration']
        self.immuneDuration = diseaseDetails['ImmuneDuration']

