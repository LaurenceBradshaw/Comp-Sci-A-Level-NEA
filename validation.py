from Framework import host, databasehandler, container, disease
import datetime


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
    if not (-180 <= coord <= 180):
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


def isIntOrFloat(data):
    if not (isinstance(data, int) or isinstance(data, float)):
        raise TypeError('Expected ' + str(float) + 'Or ' + str(int) + ' But Got ' + str(type(data)))


def isNoneNegativeInt(data):
    isInt(data)
    if data < 0:
        raise ValueError('Expected A Positive Int But Got A Negative One')


def isNoneNegativeFloat(data):
    isFloat(data)
    if data < 0:
        raise ValueError('Expected A Positive Float But Got A Negative One')


def isNoneNegativeFloatOrInt(data):
    isIntOrFloat(data)
    if data < 0:
        raise ValueError('Expected A Positive Float Or Int But Got A Negative One')


def isList(data):
    if not isinstance(data, list):
        raise TypeError('Expected ' + str(list) + ' But Got ' + str(type(data)))


def isDate(data):
    if not isinstance(data, datetime.datetime):
        raise TypeError('Expected ' + str(datetime.datetime) + ' But Got ' + str(type(data)))


def isDatabaseHandler(db):
    if not issubclass(type(db), databasehandler.DatabaseHandler):
        raise TypeError('Expected A ' + str(databasehandler.DatabaseHandler) + ' Subclass')


def isDisease(d):
    if not issubclass(type(d), disease.Disease):
        raise TypeError('Expected A ' + str(disease.Disease) + ' Subclass')


def isHost(h):
    if not issubclass(type(h), host.Host):
        raise TypeError('Expected A ' + str(host.Host) + ' Subclass')


def isContainer(c):
    if not issubclass(type(c), container.Container):
        raise TypeError('Expected A ' + str(container.Container) + ' But Got ' + str(type(c)))
