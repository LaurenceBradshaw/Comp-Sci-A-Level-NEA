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
        """
        Sets up the environments and hosts for the simulation

        :param disease: The disease class that the model will run for (disease)
        :return: One container type object to the model (container)
        """
        pass

    @abstractmethod
    def initialInfection(self, disease, topLevel):
        """
        Decides the initial infection

        :param disease: The disease class that the model will run for (disease)
        :param topLevel: The container that contains all other containers (container)
        """
        pass
