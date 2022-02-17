import unittest
from unittest.mock import MagicMock, patch, Mock
import place


class TestMatrixTests(unittest.TestCase):

    def testItShouldBeASquareMatrix(self):
        cityDetails = [["City1", 52.4862, -1.8904], ["City2", 51.4545, -2.5879], ["City3", 52.2053, 0.1218]]
        result = place.makeMatrix(cityDetails)
        self.assertEqual(len(result), len(result[0]))

    def testItShouldHaveExpectedDimensions(self):
        cityDetails = [["City1", 52.4862, -1.8904], ["City2", 51.4545, -2.5879], ["City3", 52.2053, 0.1218]]
        result = place.makeMatrix(cityDetails)
        self.assertEqual(len(result), 3)

    def testCityOutOfRange(self):
        cityDetails = [["City1", 52, 52], ["City2", 10, 10], ["City3", 43, 52]]
        self.assertRaises(ZeroDivisionError, place.makeMatrix, cityDetails)


class testCountryPopulate(unittest.TestCase):

    def setUp(self):
        self.country = place.Country("Country")

    @patch("databaseHandler.DatabaseHandler")
    @patch("place.makeMatrix")
    @patch("place.City")
    def testItGivesTheExpectedResults(self, mockCity, mockMakeMatrix, mockDb):
        mockMakeMatrix.return_value = [[]]
        mockDb.getCities.return_value = [["City1", 52.4862, -1.8904, 10], ["City2", 51.4545, -2.5879, 12], ["City3", 52.2053, 0.1218, 8]]
        self.country.populate(mockDb)
        self.assertIsNotNone(self.country.percentageMatrix)

        self.assertIsNotNone(self.country.halfwayHouses)
        self.assertEqual(len(self.country.halfwayHouses), 3)
        self.assertIsInstance(self.country.halfwayHouses[0][0], place.Building)

        self.assertIsNotNone(self.country.objects)
        self.assertEqual(len(self.country.objects), 3)
