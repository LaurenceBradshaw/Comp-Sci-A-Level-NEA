import databaseHandler
import disease
from Framework import container
from Framework import host


class OutOfRange(Exception):
    pass


def generatePoissonRange(rate):
    if not (0 < rate < 1):
        raise OutOfRange('Interaction Rate Is Out Of The Expected Range. Make Sure It Is Between 0 And 1 (Not Equal To)')


def weightedRandomRange(lb, ub, avg):
    if avg <= lb:
        raise OutOfRange('Average Is Less Than Or Equal To The Lower Bound')
    if avg >= ub:
        raise OutOfRange('Average Is Greater Than Or Equal To The Lower Bound')


def coordRange(coord):
    if not (-180 < coord < 180):
        raise OutOfRange('Coordinate Is Out Of The Expected Range')


def percentageRange(percentage):
    if not (0 <= percentage <= 100):
        raise OutOfRange('Percentage Is Out Of The Expected Range For A Percentage')


def knownActivePeriod(activePeriod):
    knownActivePeriods = ['Everyday', 'Weekdays']
    if activePeriod not in knownActivePeriods:
        raise ValueError('Not A Known Active Period')


def isString(data):
    if not isinstance(data, str):
        raise TypeError('Expected ' + str(str) + ' But Got ' + str(type(data)))


def isInt(data):
    if not isinstance(data, int):
        raise TypeError('Expected ' + str(int) + ' But Got ' + str(type(data)))


def isFloat(data):
    if not isinstance(data, float):
        raise TypeError('Expected ' + str(float) + ' But Got ' + str(type(data)))


def isList(data):
    if not isinstance(data, list):
        raise TypeError('Expected ' + str(list) + ' But Got ' + str(type(data)))


def isDatabaseHandler(db):
    if not isinstance(db, databaseHandler.DatabaseHandler):
        raise TypeError('Expected ' + str(databaseHandler.DatabaseHandler) + ' But Got ' + str(type(db)))


def isDisease(d):
    if not isinstance(d, disease.Disease):
        raise TypeError('Expected ' + str(disease.Disease) + ' But Got ' + str(type(d)))


def isHost(h):
    if not issubclass(type(h), host.Host):
        raise TypeError('Expected A ' + str(host.Host) + ' Subclass')


def isContainer(c):
    if not issubclass(type(c), container.Container):
        raise TypeError('Expected A ' + str(container.Container) + ' But Got ' + str(type(c)))
