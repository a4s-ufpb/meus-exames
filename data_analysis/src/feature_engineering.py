import numpy as np
import pandas as pd

def remove_underage(df):
    df = df[df["Age"] >= 18].copy()
    df.reset_index(drop = True, inplace= True)
    return df

def classify_hgb(df):
    condition = [
        # Homens (Sex == 0.0)
        (df["Sex"] == 0.0) & (df["HGB"] < 12),
        (df["Sex"] == 0.0) & (df["HGB"] > 15),

        # Mulheres (Sex != 0)
        (df["Sex"] != 0.0) & (df["HGB"] < 11),
        (df["Sex"] != 0.0) & (df["HGB"] > 14)

    ] 

    values = [
        0, # Homens com HGB < 12
        2, # Homens com HGB > 15
        2, # Mulheres com HGB < 11
        0 # Mulheres com HGB > 14
    ]

    df["HGB_class"] = np.select(condition, values, default=1)

    return df

def classify_pcv(df):
    condition = [
        # Homens (Sex == 0.0)
        (df["Sex"] == 0.0) & (df["PCV"] < 38.3),
        (df["Sex"] == 0.0) & (df["PCV"] > 48.6),

        # Mulheres (Sex != 0)
        (df["Sex"] != 0.0) & (df["PCV"] < 35.5),
        (df["Sex"] != 0.0) & (df["PCV"] > 44.9)
    ]

    values = [
        0, # Homens com PCV < 38.6
        2, # Homens com PCV > 48.6
        2, # Mulheres com PCV < 35.5
        0 # Mulheres com PCV > 44.9
    ]

    df["PCV_class"] = np.select(condition, values, default=1)
    return df

def classify_mchc(df):
    condition = [
        df["MCHC"] < 30,
        df["MCHC"] > 38
    ]

    values = [0,2]

    df["MCHC_class"] = np.select(condition, values, default=1)
    return df

def classify_mch(df):
    condition = [
        df["MCH"] < 25,
        df["MCH"] > 35
    ]

    values= [0,2]

    df["MCH_class"] = np.select(condition, values, default=1)
    return df

def classify_rdw(df):
    condition = [
        df["RDW"] < 12.5,
        df["RDW"] > 16
]

    values= [0,2]

    df["RDW_class"] = np.select(condition, values, default=1)
    return df

def classify_plt(df):
    condition= [
        df["PLT/mm3"] < 140,
        df["PLT/mm3"] > 450
        ]

    values = [0,2]

    df["PLT_class"] = np.select(condition, values, default=1)
    return df

def classify_rbc(df):
    condition= [
        df["RBC"] < 4,
        df["RBC"] > 5.8
    ]

    values = [0,2]

    df["RBC_class"] = np.select(condition, values, default=1)
    return df

def classify_mcv(df):
    condition = [
        df["MCV"] < 75,
        df["MCV"] > 115
    ]

    values = [0,2]

    df["MCV_class"] = np.select(condition, values, default=1)
    return df

def classify_tlc(df):
    condition = [
        df["TLC"] < 3,
        df["TLC"] > 11
    ]

    values = [0,2]

    df["TLC_class"] = np.select(condition, values, default=1)
    return df


def generate_score(df, class_columns):
    
    classification_df = df[["Name", "Sex", "Age"]+class_columns].copy()
    
    classification_df["Alteracoes"] = (classification_df[class_columns] != 1).sum(axis=1)

    classification_df["Alerta"] = np.where(
        classification_df["Alteracoes"] > 0,
        "Alterações detectadas - Procurar médico",
        "Dentro da normalidade"
    )

    return classification_df