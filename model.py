import country
import preprocessor_commond_cold as preprocessing
import plotter as pltr
from datetime import datetime, date, timedelta


class Model(object):

    def __init__(self, disease, runtime, startDate, db):
        self.startDate = date(startDate[2], startDate[1], startDate[0])
        self.disease = disease
        self.runtime = runtime
        self.housesList = []
        self.plotter = pltr.Plotter(db)
        self.db = db

    def timeStep(self, country, res, i):
        dayName = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = datetime.strptime(res, '%d-%m-%Y').weekday()
        # passes time on all places depending on the day of the week
        infected = 0
        prevInfected = 0
        prevInfected += country.getInfectedCount()
        country.timeStep(self.disease, dayName[day])
        infected += country.getInfectedCount()

        for city in country.objects:
            self.db.writeOutput(city.name, i, infected, city.getImmuneCount())

        try:
            rNaught = infected/prevInfected
        except ZeroDivisionError:
            rNaught = 0.0

        print("{} - {} ({})/({}) = ({})".format(i, dayName[day], infected, prevInfected, rNaught))

    def run(self):
        # does preprocessing (setting up all the places and people in them)
        p = preprocessing.Preprocessing(self.db)
        topLevel = p.preprocess(self.disease)
        # runs time
        i = 1
        while i <= self.runtime:
            # converts 'i' into a real date from the starting date
            resDate = self.startDate + timedelta(days=i - 1)
            res = resDate.strftime("%d-%m-%Y")
            # does the rest of the day cycle
            self.timeStep(topLevel, res, i)
            self.plotter.updateOutput(res, topLevel)
            i += 1

        self.plotter.makePlot()
        print("Model Finished")

    def increment(self, topLevel):
        # increases time infected on all people infected
        for c in topLevel.objects:
            c.increment(self.disease)

    def decrement(self, topLevel):
        # removes infected status from people who have been infected for the disease duration
        for c in topLevel.objects:
            c.decrement(self.disease)
