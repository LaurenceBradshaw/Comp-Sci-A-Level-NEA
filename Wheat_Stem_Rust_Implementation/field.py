import os
import pandas as pd
from Framework.Abstract_Classes import environment
from Wheat_Stem_Rust_Implementation import wheat


class Field(environment.Environment):

    def __init__(self, name, activePeriod, interactionRate, waterType, country, lat, lon, infectiousPeriod):
        activePeriod = [int(x) for x in activePeriod.split(',')]
        super().__init__(name, activePeriod, interactionRate)
        self.waterType = waterType
        self.name = name
        self.country = country
        self.latitude = lat
        self.longitude = lon
        self.infectiousPeriod = [int(x) for x in infectiousPeriod.split(',')]
        self.deposition = 0
        self.suitability = 0

    def timeStep(self, disease, date, uninfectedHosts, maxDeposition, species, timestepScale, probabilityThreshold):
        if date.month in self.infectiousPeriod:
            # Gets the infected host objects
            infectedHosts = self.getInfectedHosts()
            # If there are infected hosts in the environment
            if len(infectedHosts) != 0:
                # if the field is infectious
                if self.infectious():
                    for uninfectedHost in uninfectedHosts:
                        df = self._load_source_receptor_file('{}_{}'.format(self.country, self.name),
                                                             '{}_{}'.format(uninfectedHost.country, uninfectedHost.name),
                                                             species, timestepScale, self.waterType)
                        df['Hour'] = [x.split(' ')[-1].split(':')[0] for x in df['Timestamp'].values]
                        df['Year'] = [x.split(' ')[0].split('-')[0] for x in df['Timestamp'].values]
                        df['Month'] = [x.split(' ')[0].split('-')[1] for x in df['Timestamp'].values]
                        df['Day'] = [x.split(' ')[0].split('-')[2] for x in df['Timestamp'].values]
                        df = df.sort_values(by=['Year', 'Month', 'Day', 'Hour'])
                        df = df[(df['Year'].astype('int') == date.year) & (df['Month'].astype('int') == date.month) & (
                                    df['Day'].astype('int') == date.day)]
                        print(date)
                        if date.month in uninfectedHost.activePeriod:
                            print('source={}'.format(self.name))
                            print('receptor={}'.format(uninfectedHost.name))
                            print('df suitability={}'.format(df.Suitability.values[0]))
                            print('df deposition={}'.format(df.Deposition.values[0]))
                            uninfectedHost.deposition += df.Deposition.values[0]
                            uninfectedHost.suitability = df.Suitability.values[0]
                            disease.calc_relative_probability_norm(df.Deposition.values[0], df.Suitability.values[0])
                            if disease.infectionChance > 0:
                                uninfectedHost.infect()

        self.increment(disease, date)
        self.decrement(disease, date)

    # def load_data(self, source, timestep, species):
    #     '''
    #     A function that loads into memory a csv file for the processed
    #     NAME model met files from Preprocessing Step 1
    #
    #     Input args:
    #     ----------
    #     * source
    #         string of the source site to load data for
    #     * timestep
    #         string of either 'daily' or '3-hourly' to indicate the data required
    #     * species
    #         string of the rust species (only 'stem' available)
    #     '''
    #     input_file_path = '{}/{}/'.format('C:/Users/lozin/Documents/Wheat Rust/latency period', source)
    #     daily_filename = self.get_input_lp50_source_filename_daily(input_file_path,
    #                                                                     source, species)
    #     hourly3_filename = self.get_input_lp50_source_filename_3_hourly(input_file_path,
    #                                                                          source, species)
    #     if timestep == 'daily':
    #         self._load_data(daily_filename)
    #     elif timestep == '3-hourly':
    #         self._load_data(hourly3_filename)
    #     return self.df_Lp50
    #
    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    # def get_input_lp50_source_filename_daily(self, project_dir, source, species):
    #     path = '{}summary/'.format(project_dir)
    #     self.mkdir(path)
    #     species_file_string = 'lp50_{}_{}_daily.csv'.format(source, species)
    #     filename = '{}{}'.format(path, species_file_string)
    #     return filename
    #
    # def get_input_lp50_source_filename_3_hourly(self, project_dir, source, species):
    #     path = '{}summary/'.format(project_dir)
    #     self.mkdir(path)
    #     species_file_string = 'lp50_{}_{}_3_hourly.csv'.format(source, species)
    #     filename = '{}{}'.format(path, species_file_string)
    #     return filename
    #
    # def _load_data(self, filename):
    #     '''
    #     An internal function that loads into memory a netcdf file for the processed
    #     Met data temperature files from Preprocessing Step 1 if it exists, or calls the
    #     preprocessing step 1 routine to create it.
    #
    #     Input args:
    #     ----------
    #     * filename
    #         string of the filename to try loading if it exists
    #     '''
    #     print('Loading {}'.format(filename))
    #     self.df_Lp50 = pd.read_csv(filename)

    def _load_source_receptor_file(self, source, receptor, species, timestep, site_type):
        '''
        An internal function that loads in the source to receptor deposition and
        environmental suitability file for the given source and receptor

        Input args:
        ----------
        * source
            string of the source location
        * receptor
            string of the receptor location
        * species
            string of the rust species (only 'stem' available)
        * timestep
            string of either 'daily' or '3-hourly' to indicate the data required
        * site_type
            string of whether the site is 'rainfed' or 'irrigated'

        Returns:
        -------
        * df
            Pandas DataFrame of the source to receptor deposition and
            environmental suitability values
        '''
        receptor_filename = self.get_source_receptor_csv('C:/Users/lozin/Documents/Wheat Rust/',
                                                              source, receptor,
                                                              species, timestep,
                                                              site_type)
        receptor_filename += '.csv'
        print('Loading {}'.format(receptor_filename))
        df = pd.read_csv(receptor_filename)
        df.loc[df['Deposition_Log_Norm'] < 0, 'Deposition_Log_Norm'] = 0  # Correct for -inf
        df.loc[df['Suitability_Norm'] == '--', 'Suitability_Norm'] = 0  # Correct for missing data
        df.loc[df['Suitability'] == '--', 'Suitability'] = 0  # Correct for missing data
        df['Suitability'] = df['Suitability'].fillna(0)  # Correct for NaN
        df['Hour'] = [x.split(' ')[-1].split(':')[0] for x in df['Timestamp'].values]
        df['Year'] = [x.split(' ')[0].split('-')[0] for x in df['Timestamp'].values]
        df['Month'] = [x.split(' ')[0].split('-')[1] for x in df['Timestamp'].values]
        df['Day'] = [x.split(' ')[0].split('-')[2] for x in df['Timestamp'].values]
        df = df.sort_values(by=['Year', 'Month', 'Day', 'Hour'])
        return df

    def get_source_receptor_csv(self, project_dir, source, receptor, species, timestep, site_type):
        path = '{}preprocessing/'.format(project_dir)
        self.mkdir(path)
        species_file_string = '{}_deposition_from_{}_to_{}_{}_{}'.format(species, source, receptor, site_type, timestep)
        filename = '{}{}'.format(path, species_file_string)
        return filename

    def getInfectedCount(self):
        return 1 if self.hosts[0].infected else 0

    def getImmuneCount(self):
        return 1 if self.hosts[0].immune else 0

    def getInfectiousHosts(self):
        infectedHosts = []
        for h in self.hosts:
            if h.infected:
                infectedHosts.append(h)
        return infectedHosts

    def getInfectedHosts(self):
        """
        Gets the objects of the hosts which are infected

        :return: The objects of the infected hosts
        """
        infectedHosts = []
        for h in self.hosts:
            if h.infected:
                infectedHosts.append(h)
        return infectedHosts

    def infect(self):
        for host in self.hosts:
            host.infected = True

    def addHost(self):
        self.hosts.append(wheat.Wheat())

    def infected(self):
        if self.hosts[0].infected:
            return True
        else:
            return False

    def infectious(self):
        if self.hosts[0].infectious:
            return True
        else:
            return False

    def immune(self):
        if self.hosts[0].immune:
            return True
        else:
            return False

    def latencyTime(self):
        return self.hosts[0].latencyTime

    def increment(self, disease, date):
        self.hosts[0].increment(disease, date, self.activePeriod, self.infectiousPeriod)

    def decrement(self, disease, date):
        self.hosts[0].decrement(disease, date, self.activePeriod, self.infectiousPeriod)
