import pandas as pd
from os import listdir

def load_csv_data(file_name):
    

    df = pd.read_csv(file_name)

print(listdir('/'))