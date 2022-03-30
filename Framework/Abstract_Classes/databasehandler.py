from abc import ABC, abstractmethod


class DatabaseHandler(ABC):
    """
    Abstract class for accessing the database
    """
    def __init__(self):
        pass

    ##########
    # Methods
    ##########

    @abstractmethod
    def getStartDate(self):
        pass

    @abstractmethod
    def getDisease(self):
        pass

    @abstractmethod
    def getRuntime(self):
        pass

    @abstractmethod
    def writeOutput(self, cityName, time, infectedCount, immuneCount):
        pass
