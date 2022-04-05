import disease
import model
import databasehandler_country_level_implementation as db
import plotter_country_level_implementation as plt
import preprocessor_country_level_implementation as pre

if __name__ == '__main__':
    configurationNumber = 3

    # Makes a connection to the database
    dbHandler = db.DatabaseHandler(configurationNumber)
    # Gets the starting date for the simulation
    startDate = dbHandler.getStartDate()
    # Gets the amount of time that the simulation will run for
    runtime = dbHandler.getRuntime()
    # Makes the disease that the simulation will model
    disease = disease.Disease(dbHandler.getDisease())
    # Makes a plotter
    pltr = plt.Plotter(dbHandler)
    # Makes a preprocessor
    preprocess = pre.Preprocessing(dbHandler)

    # Makes the model
    model = model.Model(disease, runtime, startDate, dbHandler, pltr, preprocess)
    # Runs the model
    model.run()
