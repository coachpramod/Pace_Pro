import streamlit as st
import pandas as pd
import os
from datetime import timedelta

# 1. SET PAGE CONFIG
st.set_page_config(page_title="Pace Pro", page_icon="⚡")

# 2. FORCE COLORS WITH CSS
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #e63946 !important; }
    thead tr th { background-color: #457b9d !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

def format_pace_time(seconds):
    total_seconds = int(round(seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def calculate_pace_pro(time_str):
    try:
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 3:
            total_sec = parts[0] * 3600 + parts[1] * 60 + parts[2]
        elif len(parts) == 2:
            total_sec = parts[0] * 60 + parts[1]
        else:
            return None
        base_pace = total_sec / 10
        data_structure = [
            {"Type": "Race", "Label": "3K Pace", "Multiplier": 0.932},
            {"Type": "Race", "Label": "5K Pace", "Multiplier": 0.958},
            {"Type": "Race", "Label": "10K Pace", "Multiplier": 1.000},
            {"Type": "Race", "Label": "Half Marathon", "Multiplier": 1.045},
            {"Type": "Race", "Label": "Marathon", "Multiplier": 1.070},
            {"Type": "Training", "Label": "Easy", "Multiplier": 1.105},
            {"Type": "Training", "Label": "Steady", "Multiplier": 1.060},
            {"Type": "Training", "Label": "Threshold", "Multiplier": 0.940},
            {"Type": "Training", "Label": "Intervals", "Multiplier": 0.770},
            {"Type": "Training", "Label": "Hills Reps", "Multiplier": 0.790},
        ]
        results = [{"Category": item["Type"], "Goal": item["Label"], "Pace (/km)": format_pace_time(base_pace * item["Multiplier"])} for item in data_structure]
        return pd.DataFrame(results)
    except:
        return None

# LOGO
if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
elif os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=200)

st.title("⚡ Pace Pro: Training Calculator")
st.markdown("---")

ten_k_input = st.text_input("Enter your 10K Time (HH:MM:SS or MM:SS)", value="61:00")

if ten_k_input:
    df = calculate_pace_pro(ten_k_input)
    if df is not None:
        st.subheader("🏁 Race Goal Predictions")
        st.table(df[df['Category'] == 'Race'][['Goal', 'Pace (/km)']])
        
        st.subheader("👟 Training Zones")
        st.table(df[df['Category'] == 'Training'][['Goal', 'Pace (/km)']])
        
        st.subheader("⏱️ Track Splits")
        try:
            int_pace_str = df[df['Goal'] == 'Intervals']['Pace (/km)'].values[0]
            m_p, s_p = map(int, int_pace_str.split(':'))
            int_sec = m_p * 60 + s_p
            c1, c2, c3 = st.columns(3)
            c1.metric("400m", format_pace_time(int_sec * 0.4))
            c2.metric("800m", format_pace_time(int_sec * 0.8))
            c3.metric("1000m", format_pace_time(int_sec))
        except:
            pass

        st.divider()
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download All Paces (CSV)", data=csv_data, file_name=f"PacePro_{ten_k_input}.csv", mime='text/csv')
    else:
        st.error("Please enter a valid time (e.g., 61:00)")

