import pyodbc
import os
import validation
from Framework import databasehandler


class DatabaseHandler(databasehandler.DatabaseHandler):
    """
    Class for handling all input from and output to the database
    """
    def __init__(self, config):
        """
        Constructor of the DatabaseHandler class
        Database file path is specified
        Connection to and cursor for the database are made
        Runs the getIteration function to find the number of the simulation

        :param config: the config number of the simulation that is being run (int)
        """
        super(DatabaseHandler, self).__init__()
        # Database file path and connection string
        filename = os.path.join(os.path.expanduser("~"), "Documents/databaseRevised.accdb")
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=' + filename + ';')
        # Makes a connection to the database
        conn = pyodbc.connect(conn_str)
        # Adds a cursor to the database connection
        self.cursor = conn.cursor()
        # What configuration to use
        self.configuration = config
        # Gets the iteration of this simulation
        self.iteration = self.getIteration()

    def writeOutput(self, cityName, time, infectedCount, immuneCount):
        """
        Adds a record to the Output table in the database with the param data

        :param cityName: Name of the city this output record is for (string)
        :param time: Time elapsed in the simulation (int)
        :param infectedCount: The number of infected hosts at time param (int)
        :param immuneCount: The number of immune hosts at time param (int)
        """
        self.cursor.execute('insert into Output (Iteration, SimulationConfiguration, CityID, TimeElapsed, InfectedHosts, ImmuneHosts)'
                            'values ({},{},\'{}\',{},{},{})'.format(self.iteration, self.configuration, cityName, time, infectedCount, immuneCount))
        self.cursor.commit()

    def getIteration(self):
        """
        Selects all the records from the Output table where the TimeElapsed is 1 (to reduce the number of records returned)
        Finds the largest number and then adds one for the current simulation
        Iteration is the number of that run for the configuration

        :return: Largest iteration number + 1 (int)
        """
        self.cursor.execute('select Iteration from Output where TimeElapsed = 1 and SimulationConfiguration = {}'.format(self.configuration))
        largest = 0
        returned = self.cursor.fetchall()
        for iteration in returned:
            if iteration[0] > largest:
                largest = iteration[0]
        return largest + 1

    def getCities(self):
        """
        Selects CityID, Longitude, Latitude, CommutePercentage from the SimulationCities
        where the SimulationConfiguration is the same as was specified that this simulation will use.

        CityID is the name of the city
        CommutePercentage is the percentage of the population from the city that will travel to different cities each day

        :return: CityID, Longitude, Latitude, CommutePercentage for all cities (dict)
        """
        self.cursor.execute('select City.CityID, Longitude, Latitude, CommutePercentage '
                            'from SimulationCities inner join City '
                            'on SimulationCities.CityID = City.CityID '
                            'where SimulationConfiguration = {}'.format(self.configuration))
        result = self.cursor.fetchall()
        cityDict = {
            'CityID': [],
            'Longitude': [],
            'Latitude': [],
            'CommutePercentage': []
        }
        for row in result:
            cityDict['CityID'].append(row[0])
            cityDict['Longitude'].append(row[1])
            cityDict['Latitude'].append(row[2])
            cityDict['CommutePercentage'].append(row[3])

        return cityDict

    def getHostCount(self, cityName):
        """
        Gets the number of hosts that the specified city will contain

        :param cityName: The name of the city of which to fetch the data for (string)
        :return: the number of hosts in the specified city (int)
        """
        self.cursor.execute('select HostCount from City where CityID = \'{}\''.format(cityName))
        result = self.cursor.fetchall()[0][0]
        validation.isNoneNegativeInt(result)
        return result

    def getEnvironments(self, cityName):
        """
        Gets the environments, the number of them, and the population average and bounds,
        days where the environment is active and the interactionRate for the specified city

        :param cityName: The name of the city of which to fetch the data for (string)
        :return: EnvironmentType, Count, LowerBound, UpperBound, Average, ActivePeriod, interactionRate (dict)
        """
        self.cursor.execute('select CityEnvironments.EnvironmentType, Count, LowerBound, UpperBound, Average, ActivePeriod, interactionRate '
                            'from CityEnvironments inner join Environments on CityEnvironments.EnvironmentType = Environments.EnvironmentType '
                            'where CityEnvironments.CityID = \'{}\''.format(cityName))
        result = self.cursor.fetchall()

        dict = {
            'Type': [],
            'Count': [],
            'LowerBound': [],
            'UpperBound': [],
            'Average': [],
            'ActivePeriod': [],
            'InteractionRate': []
        }
        for row in result:
            dict['Type'].append(row[0])
            dict['Count'].append(row[1])
            dict['LowerBound'].append(row[2])
            dict['UpperBound'].append(row[3])
            dict['Average'].append(row[4])
            dict['ActivePeriod'].append(row[5])
            dict['InteractionRate'].append(row[6])
        return dict

    def getDisease(self):
        """
        Gets the information about the disease from the disease table

        :return: Duration, LatencyPeriod, InfectionChance, ImmuneDuration of the disease (dict)
        """
        self.cursor.execute('select Duration, LatencyPeriod, InfectionChance, ImmuneDuration '
                            'from Disease inner join Simulation on Disease.DiseaseID = Simulation.Disease '
                            'where SimulationConfiguration = {}'.format(self.configuration))
        result = self.cursor.fetchall()[0]
        validation.isNoneNegativeInt(result[0])
        validation.isNoneNegativeInt(result[1])
        validation.isNoneNegativeFloat(result[2])
        validation.isNoneNegativeInt(result[3])
        dict = {
            'Duration': result[0],
            'LatencyPeriod': result[1],
            'InfectionChance': result[2],
            'ImmuneDuration': result[3]
        }
        return dict

    def getRuntime(self):
        """
        Gets the runtime that the SimulationConfiguration has specified for this simulation

        :return: the simulations runtime (int)
        """
        self.cursor.execute('select RunTime from Simulation where SimulationConfiguration = {}'.format(self.configuration))
        result = self.cursor.fetchall()[0][0]
        validation.isNoneNegativeInt(result)
        return result

    def getStartDate(self):
        """
        Gets the start date that the SimulationConfiguration has specified for this simulation

        :return: the start date (list) [day, month, year]
        """
        self.cursor.execute('select StartDate from Simulation where SimulationConfiguration = {}'.format(self.configuration))
        date = self.cursor.fetchall()[0][0]
        validation.isDate(date)
        return [date.day, date.month, date.year]
