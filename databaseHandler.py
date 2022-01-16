import pyodbc


class DatabaseHandler(object):

    def __init__(self, config):
        # Makes a connection to the database
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=C:\Users\lozin\Documents\databaseRevised.accdb;')
        conn = pyodbc.connect(conn_str)
        # Adds a cursor to the database connection
        self.cursor = conn.cursor()
        # what configuration to use
        self.configuration = config
        self.iteration = self.getIteration()

    def writeOutput(self, cityName, time, infectedCount, immuneCount):
        self.cursor.execute('insert into Output (Iteration, SimulationConfiguration, CityID, TimeElapsed, InfectedHosts, ImmuneHosts)'
                            'values ({},{},\'{}\',{},{},{})'.format(self.iteration, self.configuration, cityName, time, infectedCount, immuneCount))
        self.cursor.commit()

    def getIteration(self):
        self.cursor.execute('select Iteration from Output')
        largest = 0
        returned = self.cursor.fetchall()
        for iteration in returned:
            if iteration[0] > largest:
                largest = iteration[0]
        return largest + 1

    def getCities(self):
        # returns the city names, coordinates for the simulation configuration and the percentage of people that will travel out of the city
        self.cursor.execute('select City.CityID, Longitude, Latitude, CommutePercentage '
                            'from SimulationCities inner join City '
                            'on SimulationCities.CityID = City.CityID '
                            'where SimulationConfiguration = {}'.format(self.configuration))
        return self.cursor.fetchall()

    def getHostCount(self, cityName):
        # returns the number of hosts that should be present in the specified city
        self.cursor.execute('select HostCount from City where CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()[0]

    def getEnvironments(self, cityName):
        # returns all information about all the environments in the specified city
        self.cursor.execute('select CityEnvironments.EnvironmentType, Count, LowerBound, UpperBound, Average, ActivePeriod, InfectionMultiplier '
                            'from CityEnvironments inner join Environments on CityEnvironments.EnvironmentType = Environments.EnvironmentType '
                            'where CityEnvironments.CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()

    def getCommutePercentage(self, cityName):
        # returns the percentage of the population that travel to different cities
        self.cursor.execute('select CommutePercentage from City where CityID = \'{}\''.format(cityName))
        return self.cursor.fetchall()
