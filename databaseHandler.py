import pyodbc
import os


# TODO: make abstract
class DatabaseHandler(object):
    """
    Class for handling all input from and output to the database
    """

    def __init__(self, config):
        """
        Constructor of the DatabaseHandler class
        Database file path is specified
        Connection to and cursor for the database are made
        Runs the getIteration function to find the number of the simulation

        :param config: the config number of the simulation that is being run
        """
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

        :param cityName: Name of the city this output record is for
        :param time: Time elapsed in the simulation
        :param infectedCount: The number of infected hosts at time param
        :param immuneCount: The number of immune hosts at time param
        """
        self.cursor.execute('insert into Output (Iteration, SimulationConfiguration, CityID, TimeElapsed, InfectedHosts, ImmuneHosts)'
                            'values ({},{},\'{}\',{},{},{})'.format(self.iteration, self.configuration, cityName, time, infectedCount, immuneCount))
        self.cursor.commit()

    def getIteration(self):
        """
        Selects all the records from the Output table where the TimeElapsed is 1 (to reduce the number of records returned)
        Finds the largest number and then adds one for the current simulation
        Iteration is the number of that run for the configuration

        :return: Largest iteration number + 1
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

        :return: CityID, Longitude, Latitude, CommutePercentage for all cities as pyodbc row
        """
        self.cursor.execute('select City.CityID, Longitude, Latitude, CommutePercentage '
                            'from SimulationCities inner join City '
                            'on SimulationCities.CityID = City.CityID '
                            'where SimulationConfiguration = {}'.format(self.configuration))
        return self.cursor.fetchall()

    def getHostCount(self, cityName):
        """
        Gets the number of hosts that the specified city will contain

        :param cityName: The name of the city of which to fetch the data for
        :return: the number of hosts in the specified city as an int
        """
        self.cursor.execute('select HostCount from City where CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()[0]

    def getEnvironments(self, cityName):
        """
        Gets the environments, the number of them, and the population average and bounds,
        days where the environment is active and the interactionRate for the specified city

        :param cityName: The name of the city of which to fetch the data for
        :return: EnvironmentType, Count, LowerBound, UpperBound, Average, ActivePeriod, interactionRate as a pyodbc row
        """
        self.cursor.execute('select CityEnvironments.EnvironmentType, Count, LowerBound, UpperBound, Average, ActivePeriod, interactionRate '
                            'from CityEnvironments inner join Environments on CityEnvironments.EnvironmentType = Environments.EnvironmentType '
                            'where CityEnvironments.CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()

    def getCommutePercentage(self, cityName):
        """
        Gets the percentage of the population of a city that will travel between cities

        :param cityName: The name of the city of which to fetch the data for
        :return: the percentage as a pyodbc row
        """
        self.cursor.execute('select CommutePercentage from City where CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()

    def getDisease(self):
        """
        Gets the information about the disease from the disease table

        :param disease: The name of the disease of which to fetch the data for
        :return:
        """
        self.cursor.execute('select Disease from Simulation where SimulationConfiguration = {}'.format(self.configuration))
        disease = self.cursor.fetchall()[0][0]
        self.cursor.execute('select Duration, LatencyPeriod, InfectionChance, ImmuneDuration from Disease where DiseaseID = \'{}\''.format(disease))
        return self.cursor.fetchall()[0]

    def getRuntime(self):
        """
        Gets the runtime that the SimulationConfiguration has specified for this simulation

        :return: the simulations runtime as an int
        """
        self.cursor.execute('select RunTime from Simulation where SimulationConfiguration = {}'.format(self.configuration))
        return self.cursor.fetchall()[0]

    def getStartDate(self):
        """
        Gets the start date that the SimulationConfiguration has specified for this simulation

        :return: the start date as a list [day, month, year]
        """
        self.cursor.execute('select StartDate from Simulation where SimulationConfiguration = {}'.format(self.configuration))
        date = self.cursor.fetchall()[0][0]
        return [date.day, date.month, date.year]
