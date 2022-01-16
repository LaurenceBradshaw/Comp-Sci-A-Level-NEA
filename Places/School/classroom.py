from Places import place


class Classroom(place.Place):

    def __init__(self, students):
        mixRatio = 0.7
        name = 'classroom'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        super(Classroom, self).__init__(days, students, mixRatio, name, 10, 35, 14)

