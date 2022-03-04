import unittest
from unittest.mock import MagicMock, patch, Mock
import place


class TestPopulate(unittest.TestCase):

    def setUp(self):
        self.country = place.Country("Country")

    @patch("databaseHandler.DatabaseHandler")
    @patch("place.makeMatrix")
    def testItGivesTheExpectedResults(self, mockMakeMatrix, mockDb):
        mockMakeMatrix.return_value = [[]]
        mockDb.getCities.return_value = {
            'CityID': ["City1", "City2", "City3"],
            'Longitude': [52.4862, 51.4545, 52.2053],
            'Latitude': [-1.8904, -2.5879, 0.1218],
            'CommutePercentage': [0, 0, 0]
        }
        self.country.populate(mockDb)
        self.assertEqual(len(self.country.objects), 3)


class TestConstructor(unittest.TestCase):

    def testConstructor(self):
        country = place.Country('Country')
        self.assertIsNotNone(country.percentageMatrix)
        self.assertIsNotNone(country.halfwayHouses)
