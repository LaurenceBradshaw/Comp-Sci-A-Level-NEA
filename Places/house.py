from Places import place


class House(place.Place):

    def __init__(self, people, avg):
        mixRatio = 0.8
        name = 'house'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        super(House, self).__init__(days, people, mixRatio, name, 1, 5, avg)
