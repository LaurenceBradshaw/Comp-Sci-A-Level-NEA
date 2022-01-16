from abc import ABC, abstractmethod


class Preprocessing(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def preprocess(self, disease):
        pass

    @abstractmethod
    def initialInfection(self, disease, hosts):
        pass
