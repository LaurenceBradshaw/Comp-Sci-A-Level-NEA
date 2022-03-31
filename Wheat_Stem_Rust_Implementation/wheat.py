from Framework.Abstract_Classes import host


class Wheat(host.Host):

    def __init__(self):
        super().__init__()

    def increment(self, disease, date, activePeriod):
        if self.infected and not self.immune:
            self.latencyTime += 1
        # Checks if they have been infected for the duration of the disease
        if self.latencyTime >= disease.latencyPeriod:
            if date.month in activePeriod:
                self.infectious = True
            else:
                self.immune = True

    def decrement(self, disease, date, infectiousPeriod):
        if date.month not in infectiousPeriod:
            self.immune = True
        if self.immune:
            self.latencyTime = 0
            self.infectious = False
            self.infected = False



