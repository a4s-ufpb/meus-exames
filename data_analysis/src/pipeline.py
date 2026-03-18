import os
from pathlib import Path
from data_manager import DataManager
from engine import ClinicalEngine


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "raw_data_CBC.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "clinical_features.csv"

def run_pipeline():

    dm = DataManager()
    engine = ClinicalEngine()

    try:

        df = dm.load_raw(RAW_DATA_PATH)
        df = dm.clean_numeric_data(df)

        df = dm.anonymize_patients(df)

        df = engine.classify_all_exams(df)

        df = engine.generate_health_score(df)

        dm.save_data(df, PROCESSED_DATA_PATH)

        return df

    except Exception as e:
        print(f"Erro durante a execução do pipeline: {e}")
        return None

if __name__ == "__main__":
    run_pipeline()