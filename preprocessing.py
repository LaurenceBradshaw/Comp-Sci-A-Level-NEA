import person
from Places import office, house
from Places.School import school
from Places.Shop import shop
import numpy as np
import random
import time
from Framework import preprocessor as processor


class Preprocessing(processor.Preprocessing):

    def __init__(self, args):
        super(Preprocessing, self).__init__()
        self.hostCount = args[0]
        self.officeCount = args[1]
        self.houseCount = args[2]
        self.schoolCount = args[3]
        self.shopCount = args[4]
        self.housesList = []

    def initialInfection(self, disease):
        # infects one random individual in a random house
        peopleList = []
        valid = False
        while not valid:
            x = random.randint(0, len(self.housesList) - 1)
            peopleList = self.housesList[x].people.list
            if len(peopleList) > 1:
                valid = True
        x = random.randint(0, len(peopleList) - 1)
        peopleList[x].infected = True
        peopleList[x].infectious = True
        peopleList[x].infectedTime = 1
        peopleList[x].latencyTime = disease.latencyPeriod

    def preprocess(self, disease):
        peopleList = []
        officeList = []
        schoolList = []
        shopList = []

        # make the specified number of people objects
        for _ in np.arange(0, self.hostCount):
            peopleList.append(person.Person())

        childrenList = []
        adultList = []
        retiredList = []

        # separate people by ages
        for individual in peopleList:
            if individual.age <= 18:
                childrenList.append(individual)
            elif individual.age > 65:
                retiredList.append(individual)
            else:
                adultList.append(individual)

        # make all the place objects
        sc = 1
        scAll = True
        while sc <= self.schoolCount:
            if len(childrenList) != 0:
                avg = abs(len(childrenList)/(self.schoolCount-sc+1))
                p = school.School(childrenList, adultList, avg)
                print("Number of people in school {} = {}".format(sc, p.classroomCol.getNumPeople()))
                schoolList.append(p)
            else:
                print("not enough people to fill requested number of {}".format("schools"))
                scAll = False
                break
            sc += 1
        sh = 1
        shAll = True
        while sh <= self.shopCount:
            if len(adultList) != 0:
                p = shop.Shop(adultList, peopleList)
                print("Number of staff in shop {} = {}".format(sh, len(p.staff.people.list)))
                shopList.append(p)
            else:
                print("not enough people to staff requested number of {}".format("shops"))
                shAll = False
                break
            sh += 1
        w = 1
        wAll = True
        while w <= self.officeCount:
            if len(adultList) != 0:
                p = office.Office(adultList, abs(len(adultList)/(self.officeCount-w+1)))
                print("Number of people in office {} = {}".format(w, len(p.people.list)))
                officeList.append(p)
            else:
                print("not enough people to fill requested number of {}".format("offices"))
                wAll = False
                break
            w += 1
        random.shuffle(peopleList)
        h = 1
        hAll = True
        while h <= self.houseCount:
            p = house.House(peopleList, abs(len(peopleList)/(self.houseCount-h+1)))
            if len(peopleList) != 0:
                print("Number of people in house {} = {}".format(h, len(p.people.list)))
                self.housesList.append(p)
            else:
                print("not enough people to fill requested number of {}".format("houses"))
                hAll = False
                break
            h += 1

        # people remaining not assigned to places
        if not scAll:
            print("NOT ALL SCHOOLS WERE FILLED: {}/{}".format(len(schoolList), self.schoolCount))
        else:
            print("Children remaining not in schools: {}".format(len(childrenList)))
        if not shAll:
            print("NOT ALL SHOPS WERE FILLED: {}/{}".format(len(shopList), self.shopCount))
        if not wAll:
            print("NOT ALL OFFICES WERE FILLED: {}/{}".format(len(officeList), self.officeCount))
        else:
            print("Adults remaining not in offices: {}".format(len(adultList)))
        if not hAll:
            print("NOT ALL HOUSES WERE FILLED: {}/{}".format(len(self.housesList), self.houseCount))
        else:
            print("People remaining not in houses: {}".format(len(peopleList)))
        print("Number of people retired: {}".format(len(retiredList)))
        time.sleep(5)

        # make fist infection - made on the house list to make sure its on someone who can infect others
        self.initialInfection(disease)

        # puts all places in a dictionary to return
        allPlaces = {"houses": self.housesList, "schools": schoolList, "offices": officeList, "shops": shopList}
        return allPlaces
