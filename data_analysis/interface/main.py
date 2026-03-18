import streamlit as st
import pandas as pd
from pathlib import Path
from data_analysis.interface.views.indicators import render_indicators


st.set_page_config(
    page_title="Meus Exames",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data_analysis" / "data" / "processed" / "clinical_features.csv"


@st.cache_data
def load_processed_data(path):

    if not path.exists():
        st.error(f"Arquivo não encontrado: {path}. Por favor, rode o pipeline primeiro.")
        return pd.DataFrame()

    df = pd.read_csv(path)

    if "patient_id" not in df.columns:
        df["patient_id"] = range(1, len(df) + 1)

    return df


st.title("Meus Exames")
st.markdown("---")

df = load_processed_data(DATA_PATH)

if not df.empty:
    st.sidebar.header(" Filtros")

    patient_options = df.sort_values("Name")[["patient_id", "Name"]].drop_duplicates()
    patient_map = dict(zip(patient_options["Name"], patient_options["patient_id"]))

    selected_name = st.sidebar.selectbox(
        "Escolha o paciente",
        patient_options["Name"]
    )

    patient_id = patient_map[selected_name]


    p_info = df[df["patient_id"] == patient_id].iloc[0]
    st.sidebar.markdown(f"""
    **Dados do Paciente**
    * **Nome:** {p_info['Name']}
    * **Idade:** {int(p_info['Age'])} anos
    """)


    if p_info['total_alerts'] > 0:
        st.warning(f"⚠️ {p_info['status_message']} ({int(p_info['total_alerts'])} alterações detectadas)")
    else:
        st.success(f"✅ {p_info['status_message']}")

    render_indicators(df, patient_id)
else:
    st.info("Aguardando o processamento dos dados para exibição.")