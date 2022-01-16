import pandas as pd
import matplotlib.pyplot as plt
from Framework import plotter


class Plotter(plotter.Plotter):

    def __init__(self, db):
        super(Plotter, self).__init__()
        self.db = db
        self.cities = self.db.getCities()
        self.output = []
        for _ in range(len(self.cities)):
            self.output.append(pd.DataFrame(columns=['Day', 'Infected', 'Immunities']))

    def makePlot(self):
        # outputs the final plot for each city
        cityNum = 0
        for c in self.cities:
            ax = plt.gca()

            self.output[cityNum].plot(kind='line', x='Day', y='Infected', ax=ax, color='red')
            self.output[cityNum].plot(kind='line', x='Day', y='Immunities', ax=ax, color='k')
            plt.xticks(rotation=20)

            filename = 'C:/Users/lozin/Documents/Projects/{}Output.png'.format(c[0])
            plt.savefig(filename)
            plt.close()
            cityNum += 1
            print("Plot made for {}".format(c[0]))

    def updateOutput(self, i, cities):
        # gets the number of people infected and immune people on day 'i' to plot on graph

        cityNum = 0
        for city in cities.objects:
            numInfected = 0
            numImmune = 0
            numInfected += city.getInfectedCount()
            numImmune += city.getImmuneCount()
            self.output[cityNum] = self.output[cityNum].append({'Day': i, 'Infected': numInfected, 'Immunities': numImmune},
                                                               ignore_index=True)
            cityNum += 1
