import unittest
from unittest.mock import MagicMock, patch, Mock

import functionLib


class TestCityPopulate(unittest.TestCase):

    @patch("databaseHandler.DatabaseHandler")
    def testItShouldMakeTheRightNumberOfHosts(self, mockDB):
        mockDB.getHostCount.return_value = 10
        City = functionLib.makeCity("City", 10, 10, 10)
        City.populate(mockDB)
        self.assertEqual(len(City.hosts), 10)

