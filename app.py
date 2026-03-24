import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Oxygen Cascade: Unit Reveal", layout="wide")

st.title("🫁 Oxygen Cascade: Individual Unit Reveal")
st.markdown("""
**The Challenge:** Each step is locked. To reveal a step on the graph, you must get both the **Name** and the **PO2 Value** correct (within 0.5 kPa).
""")

# --- 1. Physiological Truth ---
truth = [
    {"label": "Dry Air", "val": 21.2},
    {"label": "Trachea", "val": 19.8},
    {"label": "Alveoli", "val": 14.0},
    {"label": "Artery", "val": 13.0},
    {"label": "Capillary", "val": 7.0},
    {"label": "Vein", "val": 5.3},
    {"label": "Mitochondria", "val": 1.2}
]

true_labels = [t["label"] for t in truth]
true_vals = [t["val"] for t in truth]

# --- 2. Input Section ---
st.subheader("Enter your predictions for each unit:")
user_labels = []
user_values = []

# Using a loop to create 7 individual input rows
for i in range(len(truth)):
    cols = st.columns([2, 2, 1])
    with cols[0]:
        u_label = st.selectbox(f"Unit {i+1} Identification", 
                              options=["[Select Label]", "Alveoli", "Artery", "Dry Air", "Capillary", "Mitochondria", "Trachea", "Vein"],
                              key=f"l_{i}")
        user_labels.append(u_label)
    with cols[1]:
        u_val = st.number_input(f"Unit {i+1} PO2 (kPa)", min_value=0.0, max_value=25.0, value=0.0, step=0.1, key=f"v_{i}")
        user_values.append(u_val)
    with cols[2]:
        # Visual feedback for each row immediately after submission
        if st.session_state.get("submitted"):
            is_correct = (u_label == true_labels[i]) and (abs(u_val - true_vals[i]) <= 0.5)
            st.write("✅ Correct!" if is_correct else "❌ Locked")

# --- 3. Reveal Logic ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit and Reveal Correct Units"):
    st.session_state.submitted = True

# We only reveal the points that are 100% correct
revealed_x = []
revealed_y = []

for i in range(len(truth)):
    is_correct = (user_labels[i] == true_labels[i]) and (abs(user_values[i] - true_vals[i]) <= 0.5)
    if is_correct:
        revealed_x.append(f"Step {i+1}: {true_labels[i]}")
        revealed_y.append(true_vals[i])
    else:
        # We add a placeholder so the X-axis mapping stays consistent but the point is invisible
        revealed_x.append(f"Step {i+1}: ???")
        revealed_y.append(None)

# --- 4. Plotting ---
fig = go.Figure()

# Plot the "Guessed" path (User's raw data)
fig.add_trace(go.Scatter(
    x=[f"Step {i+1}: {l}" for i, l in enumerate(user_labels)],
    y=user_values,
    mode='lines+markers',
    name='Your Guesses',
    line=dict(color='rgba(150, 150, 150, 0.5)', dash='dot', shape='hv'),
    marker=dict(size=6, color='gray')
))

# Plot the "Revealed" units (Only the correct ones)
if st.session_state.submitted:
    fig.add_trace(go.Scatter(
        x=[f"Step {i+1}: {l}" for i, l in enumerate(user_labels)],
        y=revealed_y,
        mode='markers+text',
        name='Unlocked Units',
        text=[f"{v} kPa" if v is not None else "" for v in revealed_y],
        textposition="top center",
        marker=dict(size=18, color='#00cc96', symbol='diamond-wide', line=dict(width=2, color='white')),
    ))

fig.update_layout(
    title="Oxygen Cascade: The Unlocked Path",
    yaxis_title="PO2 (kPa)",
    template="plotly_white",
    yaxis=dict(range=[0, 25]),
    height=600,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# --- 5. Final Instructions ---
if st.session_state.submitted:
    correct_total = sum(1 for v in revealed_y if v is not None)
    if correct_total == 7:
        st.balloons()
        st.success("Congratulations! You have unlocked the entire Oxygen Cascade.")
    else:
        st.warning(f"You have unlocked {correct_total}/7 units. Adjust your incorrect guesses and submit again to reveal more!")

if st.button("Reset All Units"):
    st.session_state.submitted = False
    st.rerun()
