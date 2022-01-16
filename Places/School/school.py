from Places import place
from Places.School import staffroom, classroomcol


class School(place.Place):

    def __init__(self, students, adults, avg):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        # creates a collection of classrooms
        self.classroomCol = classroomcol.ClassroomCollection(students, 50, 900, avg)
        # gets one teacher per classroom
        teachersNeeded = len(self.classroomCol.classroomList)
        teacherList = []
        for x in range(teachersNeeded):
            teacherList.append(adults.pop(0))
        # puts teachers in a staffroom
        self.staffroom = staffroom.Staffroom(teacherList)
        # adds one teacher to each classroom
        self.classroomCol.giveTeachers(teacherList.copy())
        self.name = 'school'
        super(School, self).__init__(days)

    def timeStep(self, disease):
        # runs time on staffroom and all the classrooms
        self.staffroom.timeStep(disease)
        self.classroomCol.timeStep(disease)
