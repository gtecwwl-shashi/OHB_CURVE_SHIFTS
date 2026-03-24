import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen-Hb Masterclass", layout="wide")

st.title("🩸 Oxygen-Haemoglobin Dissociation Curve")
st.markdown("### Interactive Training: Normal vs. Clinical Shifts")

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

st.sidebar.header("2. Clinical States")
# Added Bohr Effect as a specific selectable state
curve_mode = st.sidebar.selectbox("Select Clinical State:", 
    ["Normal Physiology", "Right Shift (Bohr Effect / Fever)", "Left Shift (Alkalosis / Cold)"])

# Logic for P50 values
p50_normal = 3.6
if "Right Shift" in curve_mode:
    p50_active = 5.0
    active_color = 'crimson'
    bohr_text = "✨ **Bohr Effect Active:** ↑PCO2 and ↑H+ (lower pH) stabilize the T-state, shifting the curve RIGHT to unload O2."
elif "Left Shift" in curve_mode:
    p50_active = 2.5
    active_color = 'royalblue'
    bohr_text = "✨ **Left Shift:** ↓PCO2, ↓Temp, or ↑pH increases Hb affinity, making it 'hang on' to O2."
else:
    p50_active = 3.6
    active_color = 'black'
    bohr_text = ""

st.sidebar.header("3. Trainee Extraction")
inputs = []
for i in range(1, 7):
    val = st.sidebar.number_input(f"Doctor {i} PaO2 (kPa)", 0.0, 14.0, value=0.0, step=0.1)
    inputs.append(val)

# --- PLOTTING ---
fig = go.Figure()

# Logic for the "Reveal" button - it now shows both curves at once
reveal = st.checkbox("REVEAL CURVES (Normal vs. Active State)")

x_range = np.linspace(0.1, 14, 500)

if reveal:
    # 1. Normal Reference (Gray Dashed)
    y_ref = [calculate_sao2(x, p50_normal) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_ref, name='Normal Reference', 
                             line=dict(color='lightgray', width=2, dash='dash')))
    
    # 2. Active Clinical Curve (Bold Colored)
    y_active = [calculate_sao2(x, p50_active) for x in x_range]
    fig.add_trace(go.Scatter(x=x_range, y=y_active, name=curve_mode, 
                             line=dict(color=active_color, width=5)))

# Always plot Trainee Points if they have values
for i, val in enumerate(inputs):
    if val > 0:
        # Points are calculated against the ACTIVE curve state
        actual_sat = round(calculate_sao2(val, p50_active), 1)
        fig.add_trace(go.Scatter(x=[val], y=[actual_sat], mode='markers+text',
                                 text=[f"Dr {i+1}"], textposition="top center",
                                 marker=dict(size=14, color='black', symbol='diamond')))

# Graph Layout
fig.update_layout(
    xaxis_title=x_label if x_label else "--- ??? ---",
    yaxis_title=y_label if y_label else "--- ??? ---",
    xaxis=dict(range=[0, 14.5], tickvals=[0, 2, 4, 6, 8, 10, 12, 14], showticklabels=show_scale),
    yaxis=dict(range=[0, 105], tickvals=[0, 20, 40, 60, 80, 100], showticklabels=show_scale),
    height=750, template="plotly_white", plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)

# Bohr Effect Explanation Box
if reveal and bohr_text:
    st.info(bohr_text)
