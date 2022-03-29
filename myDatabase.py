from Framework import databasehandler
import pyodbc
import os
import validation


class myDatabase(databasehandler.DatabaseHandler):

    def __init__(self, config):
        super().__init__()
        filename = os.path.join(os.path.expanduser("~"), "Documents/wheatrustdb.accdb")
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=' + filename + ';')
        # Makes a connection to the database
        conn = pyodbc.connect(conn_str)
        # Adds a cursor to the database connection
        self.cursor = conn.cursor()
        # What configuration to use
        self.configuration = config

    def getStartDate(self):
        self.cursor.execute('select StartDate from Simulation where ID = {}'.format(self.configuration))
        date = self.cursor.fetchall()[0][0]
        validation.isDate(date)
        return date

    def getDisease(self):
        pass

    def getRuntime(self):
        self.cursor.execute('select Runtime from Simulation where ID = {}'.format(self.configuration))
        result = self.cursor.fetchall()[0][0]
        validation.isNoneNegativeInt(result)
        return result

    def getFieldData(self):
        self.cursor.execute('select * '
                            'from SimulationFields inner join Field '
                            'on SimulationFields.Field = Field.Name '
                            'where SimulationFields.ID = {}'.format(self.configuration))
        result = self.cursor.fetchall()
        return result

    def writeOutput(self, fieldName, time, infected):
        pass
