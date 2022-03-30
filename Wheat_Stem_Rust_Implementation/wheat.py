from Framework.Abstract_Classes import host


class Wheat(host.Host):

    def __init__(self):
        super().__init__()

    def increment(self, disease):
        if self.infected and not self.immune:
            self.latencyTime += 1
        # Checks if they have been infected for the duration of the disease
        if self.latencyTime >= disease.latencyPeriod:
            self.infectious = True

    def decrement(self, disease):
        if self.immune:
            self.latencyTime = 0
            self.infectious = False
            self.infected = False

