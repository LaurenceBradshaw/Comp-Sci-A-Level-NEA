import field
from Framework import container


class region(container.Container):

    def __init__(self, name):
        super().__init__(name)

    def timeStep(self, disease, day):
        pass

    def getInfectedCount(self):
        pass

    def getImmuneCount(self):
        pass

    def increment(self, disease):
        pass

    def decrement(self, disease):
        pass

    def populate(self, db):
        fieldData = db.getFieldData()
        for row in fieldData:
            self.objects.append(field.Field(row[0], row[5], 0, row[4], row[1], row[2], row[3], row[6]))
