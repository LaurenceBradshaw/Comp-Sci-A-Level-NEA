

# Objects that count as a container:
# - City (contains environments)
# - Country (contains cities)

# Preprocessing must return one container to the main model script
class Container(object):

    def __init__(self, name):
        self.objects = []
        self.name = name

    def timeStep(self, disease, day):
        for o in self.objects:
            o.timeStep(disease, day)

    def getInfectedCount(self):
        count = 0
        for o in self.objects:
            count += o.getInfectedCount()
        return count

    def getImmuneCount(self):
        count = 0
        for o in self.objects:
            count += o.getImmuneCount()
        return count

    def increment(self, disease):
        for o in self.objects:
            o.increment(disease)

    def decrement(self, disease):
        for o in self.objects:
            o.decrement(disease)

    def populate(self, db):
        pass
