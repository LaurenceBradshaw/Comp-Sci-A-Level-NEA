import unittest
from ddt import data, ddt
import validation
import datetime
from Framework import databasehandler, disease, host, container


class TestValidationGeneratePoissonRange(unittest.TestCase):

    def testItShouldRaiseOutOfRangeWhenInputIsLessThanLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.generatePoissonRange, -0.3)

    def testItShouldRaiseOutOfRangeWhenInputIsTheSameAsTheLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.generatePoissonRange, 0)

    def testItShouldNotRaiseOutOfRangeWhenInputIsInRange(self):
        try:
            validation.generatePoissonRange(0.3)
        except validation.OutOfRange:
            self.fail('generatePoissonRange Raised OutOfRange Unexpectedly')

    def testItShouldRaiseOutOfRangeWhenInputIsTheSameAsTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.generatePoissonRange, 1)

    def testItShouldRaiseOutOfRangeWhenInputIsGreaterThanTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.generatePoissonRange, 1.3)


class TestValidationWeightedRandomRange(unittest.TestCase):

    def testItShouldRaiseOutOfRangeExceptionWhenAverageIsGreaterThanTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.weightedRandomRange, 1, 3, 4)

    def testItShouldRaiseOutOfRangeExceptionWhenAverageIsLessThanTheLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.weightedRandomRange, 3, 6, 2)

    def testItShouldRaiseOutOfRangeExceptionWhenAverageIsEqualToTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.weightedRandomRange, 1, 3, 3)

    def testItShouldRaiseOutOfRangeExceptionWhenAverageIsEqualToTheLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.weightedRandomRange, 3, 6, 3)

    def testItShouldNotRaiseOutOfRangeExceptionWhenInputDataIsWithinRange(self):
        try:
            validation.weightedRandomRange(3, 5, 4)
        except validation.OutOfRange:
            self.fail('WeightedRandomRange Raised OutOfRange Unexpectedly')


class TestValidationCoordRange(unittest.TestCase):

    def testItShouldRaiseOutOfRangeWhenTheInputIsLessThanTheLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.coordRange, -200)

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsTheEqualToTheLowerBound(self):
        try:
            validation.coordRange(-180)
        except validation.OutOfRange:
            self.fail('CoordRange Raised OutOfRange Unexpectedly')

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsWithinTheRange(self):
        try:
            validation.coordRange(100)
        except validation.OutOfRange:
            self.fail('CoordRange Raised OutOfRange Unexpectedly')

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsEqualToTheUpperBound(self):
        try:
            validation.coordRange(180)
        except validation.OutOfRange:
            self.fail('CoordRange Raised OutOfRange Unexpectedly')

    def testItShouldRaiseOutOfRangeWhenTheInputIsGreaterThanTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.coordRange, 200)


class TestValidationPercentageRange(unittest.TestCase):

    def testItShouldRaiseOutOfRangeWhenTheInputIsLessThanTheLowerBound(self):
        self.assertRaises(validation.OutOfRange, validation.percentageRange, -200)

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsTheEqualToTheLowerBound(self):
        try:
            validation.percentageRange(0)
        except validation.OutOfRange:
            self.fail('PercentageRange Raised OutOfRange Unexpectedly')

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsWithinTheRange(self):
        try:
            validation.percentageRange(80)
        except validation.OutOfRange:
            self.fail('PercentageRange Raised OutOfRange Unexpectedly')

    def testItShouldNotRaiseOutOfRangeWhenTheInputIsEqualToTheUpperBound(self):
        try:
            validation.percentageRange(100)
        except validation.OutOfRange:
            self.fail('PercentageRange Raised OutOfRange Unexpectedly')

    def testItShouldRaiseOutOfRangeWhenTheInputIsGreaterThanTheUpperBound(self):
        self.assertRaises(validation.OutOfRange, validation.percentageRange, 200)


@ddt
class TestValidateKnownActivePeriod(unittest.TestCase):

    @data('Everyday', 'Weekdays')
    def testItShouldNotRaiseValueErrorForKnownActivePeriods(self, activePeriod):
        try:
            validation.knownActivePeriod(activePeriod)
        except ValueError:
            self.fail('KnownActivePeriod Raised ValueError Unexpectedly')

    def testItShouldRaiseValueErrorForAnUnknownActivePeriod(self):
        self.assertRaises(ValueError, validation.knownActivePeriod, 'NotKnown')


class TestValidateIsString(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotAString(self):
        self.assertRaises(TypeError, validation.isString, 1)

    def testItShouldNotRaiseTypeErrorWhenTheInputIsAString(self):
        try:
            validation.isString("string")
        except TypeError:
            self.fail('IsString Raised TypeError Unexpectedly')


class TestValidateIsInt(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotAnInt(self):
        self.assertRaises(TypeError, validation.isInt, "Not An Int")

    def testItShouldNotRaiseTypeErrorWhenTheInputIsAnInt(self):
        try:
            validation.isInt(1)
        except TypeError:
            self.fail('IsString Raised TypeError Unexpectedly')


class TestValidateIsFloat(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotFloat(self):
        self.assertRaises(TypeError, validation.isFloat, 1)

    def testItShouldNotRaiseTypeErrorWhenInputIsFloat(self):
        try:
            validation.isFloat(1.1)
        except TypeError:
            self.fail('IsFloat Raised TypeError Unexpectedly')


class TestIsIntOrFloat(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotIntOrFloat(self):
        self.assertRaises(TypeError, validation.isIntOrFloat, 'Not An Int Or Float')

    def testItShouldNotRaiseTypeErrorWhenInputIsAnInt(self):
        try:
            validation.isIntOrFloat(1)
        except TypeError:
            self.fail('IsIntOrFloat Raised TypeError Unexpectedly')

    def testItShouldNotRaiseTypeErrorWhenInputIsAFloat(self):
        try:
            validation.isIntOrFloat(1.2)
        except TypeError:
            self.fail('IsIntOrFloat Raised TypeError Unexpectedly')


class TestIsNoneNegativeInt(unittest.TestCase):

    def testItShouldRaiseValueErrorWhenInputIsLessThanZero(self):
        self.assertRaises(ValueError, validation.isNoneNegativeInt, -1)

    def testItShouldRaiseTypeErrorWhenInputIsNotAnInt(self):
        self.assertRaises(TypeError, validation.isNoneNegativeInt, 'Not An Int')

    def testItShouldNotRaiseValueErrorWhenInputIsPositive(self):
        try:
            validation.isNoneNegativeInt(1)
        except ValueError:
            self.fail('IsNoneNegativeInt Raised ValueError Unexpectedly')


class TestIsNoneNegativeFloat(unittest.TestCase):

    def testItShouldRaiseValueErrorWhenInputIsNegativeFloat(self):
        self.assertRaises(ValueError, validation.isNoneNegativeFloat, -1.2)

    def testItShouldRaiseTypeErrorWhenInputIsNotAFloat(self):
        self.assertRaises(TypeError, validation.isNoneNegativeFloat, 'Not A Float')

    def testItShouldNotRaiseValueErrorWhenInputIsAPositiveFloat(self):
        try:
            validation.isNoneNegativeFloat(1.5)
        except ValueError:
            self.fail('IsNoneNegativeFloat Raised ValueError Unexpectedly')


class TestIsNoneNegativeFloatOrInt(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotFloatOrInt(self):
        self.assertRaises(TypeError, validation.isNoneNegativeFloat, 'Not A Float Or Int')

    def testItShouldNotRaiseTypeErrorWhenInputIsPositiveFloat(self):
        try:
            validation.isNoneNegativeFloatOrInt(1.2)
        except TypeError:
            self.fail('IsNoneNegativeFloatOrInt Raised TypeError Unexpectedly')

    def testItShouldNotRaiseTypeErrorWhenInputIsFloat(self):
        try:
            validation.isNoneNegativeFloatOrInt(1)
        except TypeError:
            self.fail('IsNoneNegativeFloatOrInt Raised TypeError Unexpectedly')

    def testItShouldRaiseValueErrorWhenInputIsNegativeFloat(self):
        self.assertRaises(ValueError, validation.isNoneNegativeFloatOrInt, -6.3)

    def testItShouldRaiseValueErrorWhenInputIsNegativeInt(self):
        self.assertRaises(ValueError, validation.isNoneNegativeFloatOrInt, -2)


class TestIsList(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotList(self):
        self.assertRaises(TypeError, validation.isList, 3)

    def testItShouldNotRaiseTypeErrorWhenInputIsAList(self):
        try:
            validation.isList([1])
        except TypeError:
            self.fail('IsList Raised TypeError Unexpectedly')


class TestIsDate(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputIsNotDate(self):
        self.assertRaises(TypeError, validation.isDate, 'Not A Date')

    def testItShouldNotRaiseTypeErrorWhenInputIsADate(self):
        try:
            validation.isDate(datetime.datetime(2022, 3, 12))
        except TypeError:
            self.fail('IsDate Raised TypeError Unexpectedly')


class TestIsDatabaseHandler(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputAClassThatDoesNotInheritFromDatabaseHandler(self):
        self.assertRaises(TypeError, validation.isDatabaseHandler, NoneDatabaseHandler())

    def testItShouldNotRaiseTypeErrorWhenInputIsAClassThatInheritsFromDatabaseHandler(self):
        try:
            validation.isDatabaseHandler(DummyDatabaseHandler())
        except TypeError:
            self.fail('IsDatabaseHandler Raised TypeError Unexpectedly')


class TestIsDisease(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputAClassThatDoesNotInheritFromDisease(self):
        self.assertRaises(TypeError, validation.isDisease, NoneDisease())

    def testItShouldNotRaiseTypeErrorWhenInputIsAClassThatInheritsFromDisease(self):
        try:
            validation.isDisease(DummyDisease())
        except TypeError:
            self.fail('IsDisease Raised TypeError Unexpectedly')


class TestIsHost(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputAClassThatDoesNotInheritFromHost(self):
        self.assertRaises(TypeError, validation.isHost, NoneHost())

    def testItShouldNotRaiseTypeErrorWhenInputIsAClassThatInheritsFromHost(self):
        try:
            validation.isHost(DummyHost())
        except TypeError:
            self.fail('IsHost Raised TypeError Unexpectedly')


class TestIsContainer(unittest.TestCase):

    def testItShouldRaiseTypeErrorWhenInputAClassThatDoesNotInheritFromContainer(self):
        self.assertRaises(TypeError, validation.isContainer, NoneContainer())

    def testItShouldNotRaiseTypeErrorWhenInputIsAClassThatInheritsFromContainer(self):
        try:
            validation.isContainer(DummyContainer())
        except TypeError:
            self.fail('IsContainer Raised TypeError Unexpectedly')


class NoneContainer:
    pass


class DummyContainer(container.Container):

    def __init__(self):
        name = ""
        super().__init__(name)

    def timeStep(self, d, day):
        pass

    def getInfectedCount(self):
        pass

    def getImmuneCount(self):
        pass

    def increment(self, d):
        pass

    def decrement(self, d):
        pass

    def populate(self, db):
        pass


class NoneHost:
    pass


class DummyHost(host.Host):

    def increment(self, d):
        pass

    def decrement(self, d):
        pass


class NoneDisease:
    pass


class DummyDisease(disease.Disease):
    pass


class NoneDatabaseHandler:
    pass


class DummyDatabaseHandler(databasehandler.DatabaseHandler):

    def getStartDate(self):
        pass

    def getDisease(self):
        pass

    def getRuntime(self):
        pass

    def writeOutput(self, cityName, time, infectedCount, immuneCount):
        pass
