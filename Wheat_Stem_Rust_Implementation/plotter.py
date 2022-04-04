from Framework.Abstract_Classes import plotter


class Plotter(plotter.Plotter):

    def __init__(self, db):
        super(Plotter, self).__init__()
        self.db = db

    def updateOutput(self, i, topLevel):
        pass

    def makePlot(self):
        pass