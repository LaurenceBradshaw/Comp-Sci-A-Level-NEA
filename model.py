import preprocessor_commond_cold as preprocessing
import plotter as pltr
from datetime import datetime, date, timedelta
import time


class Model(object):

    def __init__(self, disease, runtime, startDate, db):
        """
        Constructor for the model class
        makes and sets all the necessary details for the model to run

        :param disease: The disease class that the model will run for (disease)
        :param runtime: The amount of time for the model to run for (int)
        :param startDate: The date at which the model will start at (list) [day, month, year]
        :param db: The class which handles all actions with the database (databaseHandler)
        """
        self.startDate = date(startDate[2], startDate[1], startDate[0])
        self.disease = disease
        self.runtime = runtime
        self.plotter = pltr.Plotter(db)
        self.db = db

    def timeStep(self, topLevel, res, i):
        """
        Simulates a day in the model

        :param topLevel: The container that contains all other containers (container)
        :param res: The date (string)
        :param i: The amount of time that the simulation has run for (int)
        """
        startTime = time.time()
        # Converts the date into a day of the week
        dayName = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = datetime.strptime(res, '%d-%m-%Y').weekday()
        # Counts the number of hosts infected before the day is simulated
        infected = 0
        prevInfected = 0
        prevInfected += topLevel.getInfectedCount()
        # Simulates the day
        topLevel.timeStep(self.disease, dayName[day])
        # Counts the number of infections after the day has been simulated
        infected += topLevel.getInfectedCount()

        # Makes an output to the database for each object contained in the top level container
        for o in topLevel.objects:
            imm = o.getImmuneCount()
            inf = o.getInfectedCount()
            self.db.writeOutput(o.name, i, inf, imm)
            print("{} - {}, {}".format(o.name, inf, imm))

        # Calculates the R number for that day
        try:
            rNaught = infected/prevInfected
        except ZeroDivisionError:
            rNaught = 0.0

        print("{} - {} ({})/({}) = ({})".format(i, dayName[day], infected, prevInfected, rNaught))
        print("Day {}: %s seconds".format(i) % (time.time() - startTime))

    def run(self):
        """
        Starts the model
        """
        startTime = time.time()
        # Makes a new instance of preprocessing
        p = preprocessing.Preprocessing(self.db)
        # Preprocessing returns one container
        topLevel = p.preprocess(self.disease)
        # Starts simulating
        i = 1
        # While the model should still be simulating
        while i <= self.runtime:
            # Converts 'i' into a real date from the starting date
            resDate = self.startDate + timedelta(days=i - 1)
            res = resDate.strftime("%d-%m-%Y")
            # Tells the top level container to simulate a day
            self.timeStep(topLevel, res, i)
            # Updates the output for plotting at the end of the models runtime
            self.plotter.updateOutput(res, topLevel)
            i += 1

        # Makes the plotter makes the plots
        self.plotter.makePlot()
        print("Model Finished")
        print("%s seconds" % (time.time() - startTime))
