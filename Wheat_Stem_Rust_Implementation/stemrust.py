from Framework.Abstract_Classes import disease
import math


class Disease(disease.Disease):

    def __init__(self, diseasedetails):
        super(Disease, self).__init__()
        self.probabilityThreshold = 0
        self.maxDeposition = 0
        self.latencyPeriod = 30

    def calc_relative_probability_norm(self, deposition, suitability):
        '''
        An internal function that calculates the normalised relative probability
        of infection

        Input args:
        ----------
        * deposition
            float of the deposition value at the receptor location
        * suitability
            float of the environmental suitability value at the receptor location

        Returns:
        -------
        * relative_probability_norm
            float of the normalised relative probability of infection
        '''
        print(deposition)
        if deposition <= 0:
            relative_probability_norm = 0
        else:
            deposition_log = math.log10(deposition)
            deposition_log_norm = (deposition_log - 0) / (math.log10(self.maxDeposition) - 0)
            suitability_norm = (suitability - 0) / (1 - 0)
            relative_probability_norm = deposition_log_norm * suitability_norm
        print('relative_probability_norm={}'.format(relative_probability_norm))
        self.infectionChance = 1 if relative_probability_norm > self.probabilityThreshold else 0
