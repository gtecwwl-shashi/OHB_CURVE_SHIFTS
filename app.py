import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🩸 Oxygen-Haemoglobin Dissociation Curve")
st.markdown("---")

# Hill Equation with adjustable P50 to demonstrate shifts
def calculate_sao2(po2_kpa, p50):
    if po2_kpa <= 0: return 0
    n_hill = 2.8 # Cooperative binding constant
    sao2 = (po2_kpa**n_hill) / ((po2_kpa**n_hill) + (p50**n_hill))
    return sao2 * 100

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("1. Axis & Scale")
x_label = st.sidebar.text_input("X-axis Label", "")
y_label = st.sidebar.text_input("Y-axis Label", "")
show_scale = st.sidebar.checkbox("Reveal Scale (0-14 kPa)", value=False)

st.sidebar.header("2. Clinical Shifts")
# Shift logic: Normal P50 is 3.6. Right shift increases P50. Left shift decreases it.
curve_mode = st.sidebar.radio("Select Curve State:", ["Normal", "Right Shift (Fever/Acidosis)", "Left Shift (Cold/Alkalosis)"])

p50_val = 3.6 # Standard
line_color = 'black'

if curve_mode == "Right Shift (Fever/Acidosis)":
    p50_val = 5.0 # Increased P50 (Reduced affinity)
    line_color = 'red'
elif curve_mode == "Left Shift (Cold/Alkalosis)":
    p50_val = 2.5 # Decreased P50 (Increased affinity)
    line_color = 'blue'

st.sidebar.header("3. Trainee Extractions")
names = ["Dr. 1", "Dr. 2", "Dr. 3", "Dr. 4", "Dr. 5", "Dr. 6"]
inputs = []
for name in names:
    inputs.append(st.sidebar.number_input(f"{name} PaO2", 0.0, 14.0, value=0.0, step=0.1))

# --- PLOTTING ---
fig = go.Figure()

# Plot Trainee Points
for i, val in enumerate(inputs):
    if val > 0:
        actual_sat = round(calculate_sao2(val, p50_val), 1)
        fig.add_trace(go.Scatter(x=[val], y=[actual_sat], mode='markers+text',
                                 text=[f"{names[i]}"], textposition="top center",
                                 marker=dict(size=15, color='crimson', symbol='diamond')))

# Graph Appearance
fig.update_layout(
    xaxis_title=x_label if x_label else "",
    yaxis_title=y_label if y_label else "",
    xaxis=dict(range=[0, 14.5], tickvals=[0, 2, 4, 6, 8, 10, 12, 14], showticklabels=show_scale),
    yaxis=dict(range=[0, 105], tickvals=[0, 20, 40, 60, 80, 100], showticklabels=show_scale),
    height=700, template="plotly_white"
)

# Reveal Curve
reveal = st.checkbox("REVEAL CURVE")
if reveal:
    x_c = np.linspace(0.1, 14, 500)
    y_c = [calculate_sao2(x, p50_val) for x in x_c]
    fig.add_trace(go.Scatter(x=x_c, y=y_c, line=dict(color=line_color, width=4), name=curve_mode))

st.plotly_chart(fig, use_container_width=True)

# --- BOHR EFFECT SECTION ---
st.markdown("---")
st.header("🦠 The Bohr Effect Explained")
col1, col2 = st.columns(2)

with col1:
    st.write("""
    The **Bohr Effect** describes how increasing **CO2** and **Hydrogen ions (H+)** specifically decrease hemoglobin's affinity for oxygen.
    
    * **At the Tissues:** High CO2/Acidity causes a **Right Shift**. Hemoglobin 'lets go' of O2 more easily.
    * **At the Lungs:** CO2 is exhaled, pH rises, causing a **Left Shift**. Hemoglobin 'grabs' O2 more easily.
    """)

with col2:
    if st.button("Simulate Bohr Effect (Tissues)"):
        st.warning("The curve just shifted RIGHT. Hemoglobin affinity has DECREASED to unload oxygen to working muscles.")
