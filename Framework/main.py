from Wheat_Stem_Rust_Implementation import stemrust as disease
import model
from Wheat_Stem_Rust_Implementation import myDatabase as db

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
