import disease
import model
import databaseHandler

if __name__ == '__main__':
    configurationNumber = 3

    # Makes a connection to the database
    dbHandler = databaseHandler.DatabaseHandler(configurationNumber)
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
