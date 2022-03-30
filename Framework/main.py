from Framework.Abstract_Classes import disease
import model
from Country_Level_Implementation import databasehandler_country_level_implementation as db

if __name__ == '__main__':
    configurationNumber = 1

    # Makes a connection to the database
    dbHandler = db.DatabaseHandler(configurationNumber)
    # Gets the starting date for the simulation
    startDate = dbHandler.getStartDate()
    # Gets the amount of time that the simulation will run for
    runtime = dbHandler.getRuntime()
    # Makes the disease that the simulation will model
    disease = disease.Disease(dbHandler.getDisease())

    # Makes the model
    model = model.Model(disease, runtime, startDate, dbHandler)
    # Runs the model
    model.run()
