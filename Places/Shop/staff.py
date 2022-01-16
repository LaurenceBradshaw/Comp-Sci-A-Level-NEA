from Places import place


class StaffSet(place.Place):

    def __init__(self, people):
        self.mixRatio = 0
        self.name = 'staff set'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        super().__init__(days, people, self.mixRatio, self.name, 4, 20, 10)
