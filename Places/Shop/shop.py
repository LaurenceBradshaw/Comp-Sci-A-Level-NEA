import random
from Places import place
from Places.Shop import customers, staff


class Shop(place.Place):

    def __init__(self, peopleToBeStaff, allPotentialCustomers):
        self.mixRatio = 0.5
        name = 'shop'
        self.staff = staff.StaffSet(peopleToBeStaff)
        self.customers = []
        self.allPotentialCustomers = allPotentialCustomers
        _ = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        super().__init__(days, _, self.mixRatio, name)

    def timeStep(self, disease):
        # get customers for the day (all people in the city)
        random.shuffle(self.allPotentialCustomers)
        self.customers = customers.CustomerSet(self.allPotentialCustomers.copy())
        # add customers to people for each day but keep same staff
        self.people.list = self.staff.people.list + self.customers.people.list
        super().timeStep(disease)
