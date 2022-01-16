from Places import place


class CustomerSet(place.Place):

    def __init__(self, people):
        self.mixRatio = 0
        name = 'customer set'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        super().__init__(days, people, self.mixRatio, name, 20, 500, 240)
