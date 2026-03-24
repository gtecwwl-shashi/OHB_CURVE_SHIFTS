import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🩸 Oxygen-Haemoglobin Dissociation Curve")
st.markdown("### Reference Mode: Compare Shifts to Normal Physiology")

# Hill Equation: p50 is the variable that shifts the curve
def calculate_sao2(po2_kpa, p50):
    if po2_kpa <= 0: return 0
    n_hill = 2.8 
    sao2 = (po2_kpa**n_hill) / ((po2_kpa**n_hill) + (p50**n_hill))
    return sao2 * 100

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("1. Identify the Graph")
x_label = st.sidebar.text_input("X-axis Label", "PaO2 (kPa)")
y_label = st.sidebar.text_input("Y-axis Label", "SaO2 (%)")
show_scale = st.sidebar.checkbox("Reveal Scale (0-14 kPa)", value=True)

st.sidebar.header("2. Clinical Shifts")
curve_mode = st.sidebar.selectbox("Select Clinical State:", 
    ["Normal (P50 = 3.6)", "Right Shift (Acidosis/Fever)", "Left Shift (Alkalosis/Cold)"])

# Logic for Shifted P50
p50_normal = 3.6
if curve_mode == "Right Shift (Acidosis/Fever)":
    p50_active = 5.0
    active_color = 'crimson'
elif curve_mode == "Left Shift (Alkalosis/Cold)":
    p50_active = 2.5
    active_color = 'royalblue'
else:
    p50_active = 3.6
    active_color = 'black'

st.sidebar.header("3. Trainee Extractions")
inputs = []
for i in range(1, 7):
    val = st.sidebar.number_input(f"Doctor {i} PaO2", 0.0, 14.0, value=0.0, step=0.1)
    inputs.append(val)

# --- PLOTTING ---
fig = go.Figure()

# ALWAYS SHOW: Normal Reference Curve (Faint Dashed Line)
x_ref = np.linspace(0.1, 14, 500)
y_ref = [calculate_sao2(x, p50_normal) for x in x_ref]
fig.add_trace(go.Scatter(x=x_ref, y=y_ref, name='Normal Reference', 
                         line
