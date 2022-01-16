from Places import place


class Staffroom(place.Place):

    def __init__(self, people):
        mixRatio = 0.5
        name = 'staffroom'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        super(Staffroom, self).__init__(days, people, mixRatio, name)
