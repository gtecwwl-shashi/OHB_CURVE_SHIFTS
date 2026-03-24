import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb & Myoglobin Masterclass", layout="wide")

st.title("🩸 Oxygen-Haemoglobin & Myoglobin Dissociation")
st.markdown("### Multi-Protein Comparison Mode")

# Hill Equation: p50 shifts the curve; n_hill determines the shape (S-shape vs Hyperbolic)
def calculate_sao2(po2_kpa, p50, n_hill=2.8):
    if po2_kpa <= 0: return 0
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

# Plot Trainee Points
for i, val in enumerate(inputs):
    if val > 0:
        actual_sat = round(calculate_sao2(val, 3.6), 1)
        fig.add_trace(go.Scatter(x=[val], y=[actual_sat], mode='markers+text',
                                 text=[f"Dr {i+1}"], textposition="top center",
                                 marker=dict(size=14, color='black', symbol='diamond')))

# --- MULTI-SELECT REVEAL ---
st.markdown("---")
st.subheader("Clinical & Protein Comparison")
selected_curves = st.multiselect(
    "Select curves to overlay:",
    ["Normal Haemoglobin (P50 3.6)", "Right Shift / Bohr Effect (P50 5.0)", "Left Shift (P50 2.5)", "Myoglobin (Hyperbolic - P50 0.3)"],
    default=[]
)

x_range = np.linspace(0.01, 14, 500)

if "Normal Haemoglobin (P50 3.6)" in selected_curves:
    y_normal = [calculate_sao2(x, 3.6, 2.8) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_normal, name='Normal Hb', 
                             line=dict(color='gray', width=3, dash='dash')))

if "Right Shift / Bohr Effect (P50 5.0)" in selected_curves:
    y_right = [calculate_sao2(x, 5.0, 2.8) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_right, name='Right Shift (Bohr)', 
                             line=dict(color='crimson', width=4)))

if "Left Shift (P50 2.5)" in selected_curves:
    y_left = [calculate_sao2(x, 2.5, 2.8) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_left, name='Left Shift', 
                             line=dict(color='royalblue', width=4)))

if "Myoglobin (Hyperbolic - P50 0.3)" in selected_curves:
    # Myoglobin uses n_hill = 1.0 because it has no cooperative binding
    y_myo = [calculate_sao2(x, 0.3, 1.0) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_myo, name='Myoglobin', 
                             line=dict(color='green', width=4)))

# Graph Layout
fig.update_layout(
    xaxis_title=x_label if x_label else "--- ??? ---",
    yaxis_title=y_label if y_label else "--- ??? ---",
    xaxis=dict(range=[0, 14.5], tickvals=[0, 2, 4, 6, 8, 10, 12, 14], showticklabels=show_scale),
    yaxis=dict(range=[0, 105], tickvals=[0, 20, 40, 60, 80, 100], showticklabels=show_scale),
    height=750, template="plotly_white", plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)

# --- EDUCATIONAL BOXES ---
if "Myoglobin (Hyperbolic - P50 0.3)" in selected_curves:
    st.success("**Myoglobin vs Haemoglobin:** Myoglobin is a monomer (n=1), so it lacks cooperative binding. This creates a **hyperbolic** curve. Its extremely low P50 (high affinity) means it only releases oxygen during severe tissue hypoxia, acting as an 'emergency reservoir' in muscles.")
