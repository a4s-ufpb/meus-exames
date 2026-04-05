import streamlit as st
from data_analysis.interface.components.bullet import plot_bullet
from data_analysis.src.config import EXAM_SETTINGS

def render_indicators(df, patient_id):

    st.subheader("Indicadores Clínicos")

    available_exams = {key: config['label'] for key, config in EXAM_SETTINGS.items()}
    
    selected_exams = st.multiselect(
        "Filtre os exames que deseja visualizar (deixe em branco para exibir todos):",
        options=list(available_exams.keys()),
        default=[],
        format_func=lambda x: available_exams[x] 
    )

    exams_to_show = selected_exams if selected_exams else list(available_exams.keys())

    cols = st.columns(3)
    charts_rendered = 0

    for exam_key in exams_to_show:
        config = EXAM_SETTINGS[exam_key]
        
        normal_range = config["ranges"].get("default", (0, 100))
        result = plot_bullet(df, patient_id, exam_key.upper(), normal_range, label=config['label'], unit=config['unit'])

        if result:
            with cols[charts_rendered % 3]:
                fig, status, color, bg_color = result

                st.plotly_chart(fig, width="stretch")

                st.markdown(
                    f"""
                    <div style="
                        background-color: {bg_color}; 
                        padding: 8px; 
                        border-radius: 5px; 
                        border-left: 5px solid {color};
                        margin-bottom: 25px;
                    ">
                        <span style="color: {color}; font-weight: bold; font-size: 0.85em;">
                            {status}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            charts_rendered += 1