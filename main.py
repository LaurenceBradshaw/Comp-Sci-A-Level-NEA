import disease
import model
import databaseHandler

if __name__ == '__main__':

    runtime = 100
    dbHandler = databaseHandler.DatabaseHandler(1)

    startDateDay = 1
    startDateMonth = 12
    startDateYear = 2020
    startDate = [startDateDay, startDateMonth, startDateYear]
    # TODO populate runtime and start date from the database

    disease = disease.Disease()
    # TODO for modeling vectors record the number of vectors that will be in each environment. Then use those numbers when infecting. instead of for each infected person it will be for each vector
    model = model.Model(disease, runtime, startDate, dbHandler)
    model.run()
