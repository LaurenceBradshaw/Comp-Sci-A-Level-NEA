from Places import place


class Office(place.Place):
    
    def __init__(self, people, avg):
        mixRatio = 0.3
        name = 'office'
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        super(Office, self).__init__(days, people, mixRatio, name, 5, 100, avg)
