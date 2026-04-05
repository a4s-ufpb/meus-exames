import math
import plotly.graph_objects as go

def plot_bullet(df, patient_id, column, normal_range, label=None, unit=None):

    df_patient = df[df["patient_id"] == patient_id]

    if df_patient.empty or column not in df_patient.columns:
        return None

    value = df_patient[column].iloc[-1]
    min_val, max_val = normal_range

    if value < min_val:
        status = "⬇ Baixo"
        color = "#f59e0b"  
        bg_color = "rgba(245, 158, 11, 0.15)"
    elif value > max_val:
        status = "⬆ Alto"
        color = "#f59e0b"  
        bg_color = "rgba(245, 158, 11, 0.15)"
    else:
        status = "✅ Normal"
        color = "#38bdf8"  
        bg_color = "rgba(56, 189, 248, 0.15)"

    axis_min = 0  
    axis_max = max(max_val * 1.5, value * 1.2)

    def get_steps(max_domain):
        if max_domain <= 0: return 5.0, 2.5
        mag = 10 ** math.floor(math.log10(max_domain))
        norm = max_domain / mag
        if norm <= 1.2: return 0.2 * mag, 0.1 * mag
        elif norm <= 2.5: return 0.5 * mag, 0.25 * mag
        elif norm <= 6.0: return 1.0 * mag, 0.5 * mag
        else: return 2.0 * mag, 1.0 * mag

    maj, min_s = get_steps(axis_max)
    
    if 15 <= axis_max <= 70:
        maj, min_s = 5.0, 2.5

    all_ticks = []
    ticktext = []
    
    curr = axis_min
    while curr <= axis_max * 1.02:
        all_ticks.append(curr)
        ratio = curr / maj
        is_major = abs(round(ratio) - ratio) < 1e-4
        
        if is_major:
            display_val = int(curr) if curr == int(curr) else round(curr, 2)
            ticktext.append(str(display_val))
        else:
            ticktext.append("")
            
        curr += min_s

    visual_clearance = (axis_max - axis_min) * 0.075 
    
    for i, t in enumerate(all_ticks):
        if ticktext[i] != "":
            if abs(t - min_val) < visual_clearance or abs(t - max_val) < visual_clearance:
                ticktext[i] = ""

    all_ticks.extend([min_val, max_val])
    ticktext.extend([
        f"<b><span style='color:#15803d'>{min_val}</span></b>", 
        f"<b><span style='color:#15803d'>{max_val}</span></b>"
    ])

    sorted_pairs = sorted(zip(all_ticks, ticktext), key=lambda x: x[0])
    all_ticks = [x[0] for x in sorted_pairs]
    ticktext = [x[1] for x in sorted_pairs]

    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        value=value,
        number={"font": {"color": color, "size": 30}},
        gauge={
            "shape": "bullet",
            "axis": {
                "range": [axis_min, axis_max],
                "tickmode": "array",  
                "tickvals": all_ticks,         
                "ticktext": ticktext,
                "ticks": "outside",
                "ticklen": 4,
                "tickcolor": "#64748b",
                "tickfont": {"size": 13, "color": "#475569"} 
            },
            "bar": {"color": color, "thickness": 0.3},
            "steps": [
                {"range": [axis_min, min_val], "color": "#f1f5f9"}, 
                {"range": [min_val, max_val], "color": "#86efac"},  
                {"range": [max_val, axis_max], "color": "#f1f5f9"},
            ]
        }
    ))

    title_text = ""
    if label and unit:
        title_text = f"<span style='color: #1e293b'><b>{label}</b></span> <span style='font-size: 13px; color: #64748b;'>({unit})</span>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.01,
            y=0.9, 
            font=dict(size=16)
        ),
        height=180,  
        margin=dict(l=15, r=25, t=55, b=25), 
        paper_bgcolor='#ffffff',  
        plot_bgcolor='#ffffff'
    )

    fig.add_annotation(
        text="<span style='color: #86efac;'>■</span> <span style='font-size: 12px; color: #64748b'>Normal</span>&nbsp;&nbsp;<span style='color: #cbd5e1;'>■</span> <span style='font-size: 12px; color: #64748b'>Fora do Padrão</span>",
        xref="paper", yref="paper",
        x=1.0, y=1.2,
        showarrow=False,
        xanchor="right", yanchor="bottom"
    )

    return fig, status, color, bg_color