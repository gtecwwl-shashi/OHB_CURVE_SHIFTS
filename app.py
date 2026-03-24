import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🩸 Oxygen-Haemoglobin Dissociation Curve")
st.markdown("### Multi-Curve Comparison Mode")

# Hill Equation: p50 is the variable that shifts the curve
def calculate_sao2(po2_kpa, p50):
    if po2_kpa <= 0: return 0
    n_hill = 2.8 
    sao2 = (po2_kpa**n_hill) / ((po2_kpa**n_hill) + (p50**n_hill))
    return sao2 * 100

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("1. Axis Setup")
x_label = st.sidebar.text_input("X-axis Label", "")
y_label = st.sidebar.text_input("Y-axis Label", "")
show_scale = st.sidebar.checkbox("Reveal Scale (0-14 kPa)", value=False)

st.sidebar.header("2. Trainee Extraction")
inputs = []
for i in range(1, 7):
    val = st.sidebar.number_input(f"Doctor {i} PaO2 (kPa)", 0.0, 14.0, value=0.0, step=0.1)
    inputs.append(val)

# --- PLOTTING ---
fig = go.Figure()

# Plot Trainee Points (Always visible once values are > 0)
for i, val in enumerate(inputs):
    if val > 0:
        # We plot these against the Normal P50 initially
        actual_sat = round(calculate_sao2(val, 3.6), 1)
        fig.add_trace(go.Scatter(x=[val], y=[actual_sat], mode='markers+text',
                                 text=[f"Dr {i+1}"], textposition="top center",
                                 marker=dict(size=14, color='black', symbol='diamond')))

# --- MULTI-SELECT REVEAL ---
st.markdown("---")
st.subheader("Clinical Comparison")
selected_curves = st.multiselect(
    "Select curves to overlay for comparison:",
    ["Normal Physiology (P50 3.6)", "Right Shift / Bohr Effect (P50 5.0)", "Left Shift (P50 2.5)"],
    default=[]
)

x_range = np.linspace(0.1, 14, 500)

if "Normal Physiology (P50 3.6)" in selected_curves:
    y_normal = [calculate_sao2(x, 3.6) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_normal, name='Normal', 
                             line=dict(color='gray', width=3, dash='dash')))

if "Right Shift / Bohr Effect (P50 5.0)" in selected_curves:
    y_right = [calculate_sao2(x, 5.0) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_right, name='Right Shift (Bohr)', 
                             line=dict(color='crimson', width=4)))

if "Left Shift (P50 2.5)" in selected_curves:
    y_left = [calculate_sao2(x, 2.5) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_left, name='Left Shift', 
                             line=dict(color='royalblue', width=4)))

# Graph Layout
fig.update_layout(
    xaxis_title=x_label if x_label else "--- ??? ---",
    yaxis_title=y_label if y_label else "--- ??? ---",
    xaxis=dict(range=[0, 14.5], tickvals=[0, 2, 4, 6, 8, 10, 12, 14], showticklabels=show_scale),
    yaxis=dict(range=[0, 105], tickvals=[0, 20, 40, 60, 80, 100], showticklabels=show_scale),
    height=700, template="plotly_white", plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)

# Bohr Effect Educational Note
if "Right Shift / Bohr Effect (P50 5.0)" in selected_curves:
    st.info("**Bohr Effect Visualized:** Notice how the Red curve sits below and to the right of the Normal curve. "
            "At any given PaO2, the hemoglobin is less saturated—meaning it has successfully released that oxygen to the tissues.")
