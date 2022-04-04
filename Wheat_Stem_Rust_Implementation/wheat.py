from Framework.Abstract_Classes import host


class Wheat(host.Host):

    def __init__(self):
        super().__init__()

    def increment(self, disease, date, activePeriod, infectiousPeriod):
        # If there is no crop in the field to infect
        if date.month not in activePeriod:
            self.immune = True
        # If it can't be infectious
        if date.month not in infectiousPeriod:
            self.infectious = False

        # If it is infected and there is crop in the field
        if self.infected and not self.immune:
            self.latencyTime += 1

        # Checks if they have been infected for the duration of the disease
        if self.latencyTime >= disease.latencyPeriod:
            if not self.immune:
                self.infectious = True
            else:
                self.immune = True

    def decrement(self, disease, date, activeperiod, infectiousPeriod):
        # If there is crop in the field
        if date.month in activeperiod:
            self.immune = False

        # If there is no crop in the field
        if self.immune:
            self.latencyTime = 0
            self.infectious = False
            self.infected = False
