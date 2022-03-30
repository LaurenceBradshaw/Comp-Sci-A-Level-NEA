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
    def updateOutput(self, i, topLevel):
        """
        Updates the output data for the end graph

        :param i: Time passed in the simulation (int)
        :param topLevel: The container that contains all other containers (container)
        """
        pass

    @abstractmethod
    def makePlot(self):
        """
        Makes the final plot
        """
        pass
