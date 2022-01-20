import disease
import model
import databaseHandler

if __name__ == '__main__':
    configurationNumber = 1

    dbHandler = databaseHandler.DatabaseHandler(configurationNumber)
    startDate = dbHandler.getStartDate()
    runtime = dbHandler.getRuntime()[0]
    disease = disease.Disease(dbHandler.getDisease("Common Cold"))

    # TODO for modeling vectors record the number of vectors that will be in each environment. Then use those numbers when infecting. instead of for each infected person it will be for each vector
    model = model.Model(disease, runtime, startDate, dbHandler)
    model.run()
