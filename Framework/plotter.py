from abc import ABC, abstractmethod


class Plotter(ABC):

    def __init__(self):
        self._output = None

    @abstractmethod
    def updateOutput(self, i, environments):
        pass

    @abstractmethod
    def makePlot(self):
        pass
