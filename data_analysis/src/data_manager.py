import pandas as pd
import numpy as np
from faker import Faker
import os


class DataManager:
    def __init__(self, locale='pt-BR'):
        self.faker = Faker(locale)

    def load_raw(self, path):

        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        df = pd.read_csv(path)

        df.columns = df.columns.str.strip().str.replace(' ', '')
        return df

    def clean_numeric_data(self, df):

        df = df.copy()

        for char in ['-', ',', '%']:
            df = df.replace(char, '', regex=True)

        df = df.replace('', np.nan)
        df = df.dropna()


        cols_to_fix = df.columns.difference(['Sex', 'Age', 'Name'])
        df[cols_to_fix] = df[cols_to_fix].apply(pd.to_numeric, errors='coerce')

        return df.dropna()

    def anonymize_patients(self, df):

        df = df.copy()
        names = []
        for _, row in df.iterrows():

            if row['Sex'] == 0:
                names.append(self.faker.name_male())
            else:
                names.append(self.faker.name_female())

        df['Name'] = names

        if 'patient_id' not in df.columns:
            df['patient_id'] = range(1, len(df) + 1)

        return df

    def save_data(self, df, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)