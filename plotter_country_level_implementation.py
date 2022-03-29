import pandas as pd
import matplotlib.pyplot as plt
from Framework import plotter
import os


class Plotter(plotter.Plotter):
    """
    Class which does all the plotting for the model
    """
    def __init__(self, db):
        """
        Constructor for the plotter

        :param db: The class which handles all interactions with the database (databaseHandler)
        """
        super(Plotter, self).__init__()
        self.db = db
        self.cities = self.db.getCities()
        self.output = []
        for _ in range(len(self.cities)):
            self.output.append(pd.DataFrame(columns=['Day', 'Infected', 'Immunities']))

    def makePlot(self):
        """
        Outputs the final plot for each city once the simulation has finished running
        """
        for i in range(len(self.cities['CityID'])):
            ax = plt.gca()

            self.output[i].plot(kind='line', x='Day', y='Infected', ax=ax, color='red')
            self.output[i].plot(kind='line', x='Day', y='Immunities', ax=ax, color='k')
            plt.xticks(rotation=20)

            filename = os.path.join(os.getcwd(), "Output/{}Output.png".format(self.cities['CityID'][i]))
            plt.savefig(filename)
            plt.close()
            print("Plot made for {}".format(self.cities['CityID'][i]))

    def updateOutput(self, i, topLevel):
        """
        Updates the pandas dataframe with the hosts infected and immune for the day that was just simulated

        :param i: The number of days passed since the simulation started (int)
        :param topLevel: The container that contains all other containers (container)
        """
        for num, city in enumerate(topLevel.objects):
            self.output[num] = self.output[num].append({'Day': i, 'Infected': city.getInfectedCount(), 'Immunities': city.getImmuneCount()}, ignore_index=True)
