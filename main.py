import disease
import model
import databaseHandler

if __name__ == '__main__':
    numPeople = 130000
    numWorkplaces = 2100
    numHouses = 51499
    numSchools = 42
    numShops = 40

    runtime = 200
    dbHandler = databaseHandler.DatabaseHandler(1)

    startDateDay = 1
    startDateMonth = 12
    startDateYear = 2020
    startDate = [startDateDay, startDateMonth, startDateYear]

    disease = disease.Disease()
    # TODO for modeling vectors record the number of vectors that will be in each environment. Then use those numbers when infecting. instead of for each infected person it will be for each vector
    model = model.Model(disease, runtime, startDate, dbHandler)
    model.run()
