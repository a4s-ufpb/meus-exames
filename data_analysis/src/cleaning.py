import pandas as pd
import numpy as np
from faker import Faker

def load_raw_data(path):
    return pd.read_csv(path)

def clean_dataframe(df):
    df = df.copy()

    df.columns = df.columns.str.replace(' ','')
    df = df.replace('-', '', regex=True)
    df = df.replace(',','', regex=True)
    df = df.replace('%','', regex=True)
    df = df.replace('', np.nan)

    df = df.dropna()
    df = df.astype("float64")

    return df

def generate_names(df):

    faker = Faker('pt-BR')

    names = []

    for i, row in df.iterrows():
        if row['Sex'] == 0:
            names.append(faker.name_male())
        else:
            names.append(faker.name_female())


    df['Name'] = names
    return df

def save_cleaned_data(df, path):
    df.to_csv(path, index=False)