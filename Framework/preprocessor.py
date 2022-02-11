from abc import ABC, abstractmethod


class Preprocessing(ABC):
    """
    Abstract class for preprocessing
    """
    def __init__(self):
        """
        Constructor for preprocessing
        """
        pass

    ##########
    # Methods
    ##########

    @abstractmethod
    def preprocess(self, disease):
        pass

    @abstractmethod
    def initialInfection(self, disease, hosts):
        pass
