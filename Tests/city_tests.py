import unittest
from unittest.mock import MagicMock, patch, Mock
import functionLib
import place


class TestConstructor(unittest.TestCase):

    def testConstructorIsAssigningAndMakingProperly(self):
        city = functionLib.makeCity("City", 1, 5, 10)
        self.assertEqual(city.name, "City")
        self.assertEqual(city.longitude, 1)
        self.assertEqual(city.latitude, 5)
        self.assertEqual(city.commutePercentage, 10)
        self.assertIsNotNone(city.commutePercentage)
        self.assertIsNotNone(city.hosts)
        self.assertIsNotNone(city.shopRange)


class TestCityPopulate(unittest.TestCase):

    @patch("databaseHandler.DatabaseHandler")
    def testItShouldMakeTheRightNumberOfHosts(self, mockDB):
        mockDB.getHostCount.return_value = 10
        City = functionLib.makeCity("City", 10, 10, 10)
        City.populate(mockDB)
        self.assertEqual(len(City.hosts), 10)

    @patch("databaseHandler.DatabaseHandler")
    def testItMakesABuildingAsExpectedWhenNotAShop(self, mockDB):
        mockDB.getEnvironments.return_value = [["House", 10, 1, 6, 4, "Everyday", 0.7]]
        City = functionLib.makeCity("City", 10, 10, 10)
        City.populate(mockDB)
        self.assertEqual(len(City.objects), 10)
        self.assertIsInstance(City.objects[0], place.Building)
        self.assertEqual(City.objects[0].activePeriod, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.assertEqual(City.objects[0].interactionRate, 0.7)

    @patch("databaseHandler.DatabaseHandler")
    def testItMakesABuildingAsExpectedWhenAShop(self, mockDB):
        mockDB.getEnvironments.return_value = [["Shop", 10, 1, 6, 4, "Everyday", 0.3]]
        City = functionLib.makeCity("City", 10, 10, 10)
        City.populate(mockDB)
        self.assertEqual(len(City.objects), 10)
        self.assertIsInstance(City.objects[0], place.Building)
        self.assertEqual(City.shopRange, [1, 6, 4])
        self.assertEqual(len(City.objects[0].hosts), 0)
        self.assertEqual(City.objects[0].activePeriod, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        self.assertEqual(City.objects[0].interactionRate, 0.3)

