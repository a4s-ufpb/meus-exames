import plotly.graph_objects as go


def plot_bullet(df, patient_id, column, normal_range):

    df_patient = df[df["patient_id"] == patient_id]

    if df_patient.empty or column not in df_patient.columns:
        return None


    value = df_patient[column].iloc[-1]
    min_val, max_val = normal_range


    if value < min_val:
        status = "Baixo!"
        color = "#ff4b4b"  # Vermelho (Streamlit Standard)
        bg_color = "rgba(255, 75, 75, 0.1)"
    elif value > max_val:
        status = "Alto!"
        color = "#ffa500"  # Laranja
        bg_color = "rgba(255, 165, 0, 0.1)"
    else:
        status = "Normal"
        color = "#00c04b"  # Verde (Padronizado para saúde)
        bg_color = "rgba(0, 192, 75, 0.1)"  # Verde suave para o fundo


    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=value,
        gauge={
            "shape": "bullet",
            "axis": {"range": [0, max_val * 1.5]},  # Eixo dinâmico baseado no limite
            "steps": [
                {"range": [0, min_val], "color": "#e00d0d"},  # Zona Vermelha
                {"range": [min_val, max_val], "color": "#00c04b"},  # Zona Verde
                {"range": [max_val, max_val * 1.5], "color": "#ffa500"},  # Zona Amarela
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "value": value
            }
        }
    ))


    fig.update_layout(
        height=120,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente para o Plotly
        plot_bgcolor='rgba(0,0,0,0)'
    )


    return fig, status, color, bg_color