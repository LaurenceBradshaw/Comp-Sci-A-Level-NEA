import databaseHandler
import disease


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


def isString(data):
    if not isinstance(data, str):
        raise TypeError('Expected A String But Got ' + str(type(data)))


def isInt(data):
    if not isinstance(data, int):
        raise TypeError('Expected An Integer But Got ' + str(type(data)))


def isFloat(data):
    if not isinstance(data, float):
        raise TypeError('Expected A Float But Got ' + str(type(data)))


def isList(data):
    if not isinstance(data, list):
        raise TypeError('Expected A List But Got ' + str(type(data)))


def isDatabaseHandler(db):
    if not isinstance(db, databaseHandler.DatabaseHandler):
        raise TypeError('Expected A Database Handler But Got ' + str(type(db)))


def isDisease(d):
    if not isinstance(d, disease.Disease):
        raise TypeError('Expected A Disease But Got ' + str(type(d)))
