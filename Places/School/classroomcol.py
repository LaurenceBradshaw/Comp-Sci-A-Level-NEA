import numberHandler
from Places.School import classroom


class ClassroomCollection(object):

    def __init__(self, students, lb, ub, avg):
        self.classroomList = []
        self.students = []
        for _ in range(min(numberHandler.weightedRandom(lb, ub, avg), len(students))):
            self.students.append(students.pop(0))
        self.createClassrooms(self.students)

    def createClassrooms(self, students):
        while len(students) > 0:
            self.classroomList.append(classroom.Classroom(students))

    def giveTeachers(self, adults):
        for c in self.classroomList:
            c.people.list.append(adults.pop(0))

    def timeStep(self, disease):
        for cr in self.classroomList:
            cr.timeStep(disease)

    def getNumPeople(self):
        n = 0
        for c in self.classroomList:
            n += len(c.people.list)
        return n
