import numberHandler


class People(object):

    def __init__(self):
        self.list = []

    def getUninfectedPeople(self):
        # gets all the uninfected people
        uninfectedPeopleList = []
        for p in self.list:
            if not p.infected and not p.immune:
                uninfectedPeopleList.append(p)
        return uninfectedPeopleList

    def getInfectedPeople(self):
        # gets all infected people
        infectedPeopleList = []
        for p in self.list:
            if p.infected:
                infectedPeopleList.append(p)
        return infectedPeopleList

    def populate(self, people, lb, ub, avg):
        # gets the number of people based off a normal distribution with a cut off at 'peopleLower' and 'peopleUpper'
        for x in range(min(numberHandler.weightedRandom(lb, ub, avg), len(people))):
            try:
                self.list.append(people.pop(0))
            except IndexError:
                break
        return people
