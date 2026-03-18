import streamlit as st
from data_analysis.interface.components.bullet import plot_bullet
from data_analysis.src.config import EXAM_SETTINGS


def render_indicators(df, patient_id):

    st.subheader("Indicadores Clínicos")


    st.markdown("""
        <div style="display: flex; gap: 15px; margin-bottom: 20px; font-size: 0.8em; color: #888;">
            <span><span style="color: #e00d0d;">■</span> Baixo</span>
            <span><span style="color: #00c04b;">■</span> Normal</span>
            <span><span style="color: #ffa500;">■</span> Alto</span>
        </div>
    """, unsafe_allow_html=True)


    cols = st.columns(3)

    for i, (exam_key, config) in enumerate(EXAM_SETTINGS.items()):
        with cols[i % 3]:

            st.markdown(f"**{config['label']}** <small>({config['unit']})</small>", unsafe_allow_html=True)

            normal_range = config["ranges"].get("default", (0, 100))
            result = plot_bullet(df, patient_id, exam_key.upper(), normal_range)

            if result:

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
            else:
                st.info(f"Dados de {config['label']} indisponíveis.")

            st.write("")