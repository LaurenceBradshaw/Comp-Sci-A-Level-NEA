from Framework import validation
from Framework.Abstract_Classes import databasehandler
import pyodbc
import os
import numpy


class DatabaseHandler(databasehandler.DatabaseHandler):

    def __init__(self, config):
        super().__init__()
        filename = os.path.join(os.path.expanduser("~"), "Documents/Wheat Rust/wheatrustdb.accdb")
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'+
                    r'DBQ=' + filename + ';')
        # Makes a connection to the database
        conn = pyodbc.connect(conn_str)
        # Adds a cursor to the database connection
        self.cursor = conn.cursor()
        # What configuration to use
        self.configuration = config
        self.iteration = self.getIteration()

    def getStartDate(self):
        self.cursor.execute('select StartDate from Simulation where ID = {}'.format(self.configuration))
        date = self.cursor.fetchall()[0][0]
        validation.isDate(date)
        return date

    def getIteration(self):
        """
        Selects all the records from the Output table where the TimeElapsed is 1 (to reduce the number of records returned)
        Finds the largest number and then adds one for the current simulation
        Iteration is the number of that run for the configuration

        :return: Largest iteration number + 1 (int)
        """
        self.cursor.execute('select Iteration from Output where TimeElapsed = 1 and ID = {}'.format(self.configuration))
        largest = 0
        returned = self.cursor.fetchall()
        for iteration in returned:
            if iteration[0] > largest:
                largest = iteration[0]
        return largest + 1

    def getDisease(self):
        return ""

    def getRuntime(self):
        self.cursor.execute('select Runtime from Simulation where ID = {}'.format(self.configuration))
        result = self.cursor.fetchall()[0][0]
        validation.isNoneNegativeInt(result)
        return result

    def getFieldData(self):
        self.cursor.execute('select Name, ReceptiveMonths, WaterType, Country, Latitude, Longitude, InfectiousMonths '
                            'from SimulationFields inner join Field '
                            'on SimulationFields.Field = Field.Name '
                            'where SimulationFields.ID = {}'.format(self.configuration))
        result = self.cursor.fetchall()
        return result

    def getStartingSources(self):
        self.cursor.execute('select Field from SimulationFields where StartingSource = true and SimulationFields.ID = {}'.format(self.configuration))
        result = self.cursor.fetchall()
        return result

    def getSimulationParameters(self):
        self.cursor.execute('select ProbabilityThreshold, Species, Timestep from Simulation where Simulation.ID = {}'.format(self.configuration))
        result1 = self.cursor.fetchall()[0]
        self.cursor.execute('select MaxDeposition from Simulation where Simulation.ID = {}'.format(self.configuration))
        result2 = int(self.cursor.fetchall()[0][0])
        result = [result2, result1[0], result1[1], result1[2]]
        return result

    def writeOutput(self, fieldName, time, infected, immune):
        self.cursor.execute(
            'insert into Output (Iteration, ID, Field, TimeElapsed, Infected, Immune)'
            'values ({},{},\'{}\',{},{},{})'.format(self.iteration, self.configuration, fieldName, time, infected,
                                                    immune))
        self.cursor.commit()
