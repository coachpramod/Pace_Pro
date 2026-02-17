import streamlit as st

# --- LOGIC FUNCTIONS ---
def format_pace(decimal_minutes):
    """Converts decimal minutes (e.g., 7.5) to MM:SS string."""
    if decimal_minutes < 0: return "0:00"
    minutes = int(decimal_minutes)
    seconds = int(round((decimal_minutes - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"

# --- WEB UI SETUP ---
st.set_page_config(page_title="Pace Pro 2026", page_icon="🏃‍♂️")

# Custom CSS to match your Dark Blue/Teal aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #031633; color: white; }
    .stNumberInput label { color: white !important; }
    .stButton>button { background-color: #1e90ff; color: white; width: 100%; border-radius: 5px; border: none; font-weight: bold; }
    .pace-header { color: #00ced1; font-weight: bold; font-size: 1.2rem; border-bottom: 2px solid #00ced1; margin-top: 25px; margin-bottom: 10px; }
    .pace-row { font-family: 'Courier New', Courier, monospace; font-size: 1.1rem; padding: 5px 0; border-bottom: 1px solid #1a2a44; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃‍♂️ PACE PRO CALCULATOR")
st.write("Professional Training & Race Pace Strategy")

# --- INPUT SECTION ---
target_10k = st.number_input("Enter 10K Target Time (Total Minutes):", min_value=1.0, value=71.0, step=0.1)

# --- CALCULATIONS ---
# Base formula: (Target / 10)
base = target_10k / 10

race_paces = {
    "10K Pace": base * 1.0,
    "Marathon": base * 1.085,
    "Half Marathon": base * 1.05,
    "5K Pace": base * 0.96,
    "3K Pace": base * 0.93,
}

train_zones = {
    "Easy (Aerobic)": base * 1.22,
    "Steady": base * 1.07,
    "Threshold": base * 0.965,
    "Hills Reps": base * 0.88,
    "Intervals / Reps": base * 0.85
}

# --- DISPLAY RESULTS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="pace-header">RACE PACES</p>', unsafe_allow_html=True)
    for name, pace in race_paces.items():
        st.markdown(f'<div class="pace-row"><b>{name}:</b> {format_pace(pace)} /km</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p class="pace-header">TRAINING ZONES</p>', unsafe_allow_html=True)
    for name, pace in train_zones.items():
        st.markdown(f'<div class="pace-row"><b>{name}:</b> {format_pace(pace)} /km</div>', unsafe_allow_html=True)

st.info("Formulas applied: ($B$1/10) multiplied by intensity factors.")
