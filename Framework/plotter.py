from abc import ABC, abstractmethod


class Plotter(ABC):
    """
    Abstract class for plotting
    """
    def __init__(self):
        """
        Constructor for plotter
        """
        self._output = None

    ##########
    # Methods
    ##########

    @abstractmethod
    def updateOutput(self, i, environments):
        pass

    @abstractmethod
    def makePlot(self):
        pass
