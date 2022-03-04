import unittest
from unittest.mock import MagicMock, patch, Mock
import functionLib
import place
from person import Person


class TestMakeMatrix(unittest.TestCase):

    def testItShouldNotBeNone(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        result = functionLib.makeMatrix(cityDetails)
        self.assertIsNotNone(result)

    def testItShouldBeASquareMatrix(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        result = functionLib.makeMatrix(cityDetails)
        self.assertEqual(len(result), len(result[0]))

    def testItShouldHaveExpectedDimensions(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        result = functionLib.makeMatrix(cityDetails)
        self.assertEqual(len(result), 3)

    def testCityOutOfRange(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52, 10, 43],
            'Latitude': [52, 10, 52]
        }
        self.assertRaises(ZeroDivisionError, functionLib.makeMatrix, cityDetails)


class TestGeneratePoisson(unittest.TestCase):

    @patch('random.randint')
    def testItShouldHaveKnownResultWhenInRange(self, rng):
        rng.return_value = 50
        result = functionLib.generatePoisson(0.3)
        self.assertAlmostEqual(result, 0.9761355487, 10)

    @patch('random.randint')
    def testItShouldRaiseRateOutOfRangeExceptionWhenAboveRange(self, rng):
        rng.return_value = 50
        self.assertRaises(functionLib.RateOutOfRange, functionLib.generatePoisson, 1.1)

    @patch('random.randint')
    def testItShouldRaiseRateOutOfRangeExceptionWhenBelowRange(self, rng):
        rng.return_value = 50
        self.assertRaises(functionLib.RateOutOfRange, functionLib.generatePoisson, -0.3)

    @patch('random.randint')
    def testItShouldRaiseRateOutOfRangeExceptionWhenLowerBoundOfRange(self, rng):
        rng.return_value = 50
        self.assertRaises(functionLib.RateOutOfRange, functionLib.generatePoisson, 0)

    @patch('random.randint')
    def testItShouldRaiseRateOutOfRangeExceptionWhenUpperBoundOfRange(self, rng):
        rng.return_value = 50
        self.assertRaises(functionLib.RateOutOfRange, functionLib.generatePoisson, 1)


class TestCoordsToDistance(unittest.TestCase):

    def testItShouldHaveKnownValue(self):
        result = functionLib.coordsToDistance(52.4862, 51.4545, -1.8904, -2.5879)
        self.assertAlmostEqual(result, 138.4, 1)


class TestHalfwayHouseMatrix(unittest.TestCase):

    def testItShouldNotBeNone(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        halfwayHouses = functionLib.makeHalfwayHouses(cityDetails)
        self.assertIsNotNone(halfwayHouses)

    def testItShouldBeASquareMatrix(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        halfwayHouses = functionLib.makeHalfwayHouses(cityDetails)
        self.assertEqual(len(halfwayHouses), len(halfwayHouses[0]))

    def testItShouldHaveExpectedDimensions(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        halfwayHouses = functionLib.makeHalfwayHouses(cityDetails)
        self.assertEqual(len(halfwayHouses), 3)

    def testItShouldContainABuilding(self):
        cityDetails = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218]
        }
        halfwayHouses = functionLib.makeHalfwayHouses(cityDetails)
        self.assertIsInstance(halfwayHouses[0][0], place.Building)


class TestSortHosts(unittest.TestCase):

    def testItShouldSortTheHostsCorrectly(self):
        hosts = [Person(), Person(), Person(), Person(), Person(), Person()]
        hosts[0].age = 4  # school
        hosts[1].age = 18  # school
        hosts[2].age = 20  # office
        hosts[3].age = 65  # office
        hosts[4].age = 70  # none
        hosts[5].age = 9999999999999999999  # none
        result = functionLib.sortHosts(hosts)
        self.assertEqual(len(result["House"]), 6)
        self.assertEqual(len(result["Office"]), 2)
        self.assertEqual(len(result["School"]), 2)

