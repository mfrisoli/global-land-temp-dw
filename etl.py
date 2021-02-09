from helpers.get_kaggle_data import kaggle_download
import os
import pandas as pd


# Download Data from Kaggle API
# kaggle_download('berkeleyearth/climate-change-earth-surface-temperature-data')

# TODO: Read CSV files tables
directory = os.path.realpath("..") + '/global-land-temp-dw/data/'
tables = ['GlobalLandTemperaturesByMajorCity.csv',
          'GlobalLandTemperaturesByCity.csv']


for table in tables:
    df = pd.read_csv(directory + table)
    print(df.head())

# TODO: Datawrangle each table
# TODO: Create schema and stage data
# TODO: Insert data to the schema
