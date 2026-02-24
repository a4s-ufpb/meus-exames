from cleaning import load_raw_data, clean_dataframe, generate_names, save_cleaned_data
from feature_engineering import remove_underage, classify_hgb, classify_mchc, classify_mch, classify_mcv, classify_pcv, classify_plt, classify_rbc, classify_rdw, classify_tlc, generate_score
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH =  BASE_DIR /"data"/"raw"/"raw_data_CBC.csv"
CLEAN_PATH = BASE_DIR /"data"/"processed"/"cleaned_data.csv"
FEATURE_PATH = BASE_DIR /"data"/"processed"/"clinical_features.csv"

def main():
    df = load_raw_data(RAW_PATH)

    df = clean_dataframe(df)
    df = generate_names(df)

    save_cleaned_data(df, CLEAN_PATH)

    df = remove_underage(df)

    df = classify_hgb(df)
    df = classify_mch(df)
    df = classify_mchc(df)
    df = classify_mcv(df)
    df = classify_pcv(df)
    df = classify_plt(df)
    df = classify_rbc(df)
    df = classify_rdw(df)
    df = classify_tlc(df)

    class_columns = [
        "HGB_class",
        "PCV_class",
        "MCHC_class",
        "MCH_class",
        "RDW_class",
        "PLT_class",
        "RBC_class",
        "MCV_class",
        "TLC_class"
    ]

    df = generate_score(df, class_columns)
    df.to_csv(FEATURE_PATH, index=False)

if __name__ == "__main__":
    main()