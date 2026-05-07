import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="IPL Predictor", layout="centered")

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(180deg, #0b1120, #0f172a);
    color: #e5e7eb;
}

/* ===== TITLE ===== */
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: white !important;
}
/* ===== SUBTITLE ===== */
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}

/* ===== LABELS ===== */
label {
    color: #cbd5e1 !important;
    font-size: 13px;
}

/* ===== INPUTS ===== */
div[data-baseweb="input"] input {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    height: 38px;
}

/* ===== SELECT ===== */
div[data-baseweb="select"] {
    background-color: #1f2937 !important;
    border-radius: 6px;
}

/* ===== BUTTON ===== */
div.stButton > button {
    border: 1px solid #4b5563;
    color: white;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    border-radius: 8px;
    width: 100%;
    height: 45px;
    font-size: 16px;
    font-weight: 600;
}

/* ===== RESULT ===== */
.result {
    text-align: center;
    font-size: 30px;
    font-weight: 600;
    margin-top: 30px;
}

/* ===== SECTION HEADINGS ===== */
.section {
    text-align: center;
    color: #ffcc00;
    font-size: 30px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<h1>🏏 IPL Win Probability Predictor</h1>", unsafe_allow_html=True)

st.markdown(
    "<div class='subtitle'>Real-time match prediction using Machine Learning</div>",
    unsafe_allow_html=True
)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("model.pkl", "rb"))

# =========================
# DATA
# =========================
teams = [
    'Chennai Super Kings',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Delhi Capitals',
    'Sunrisers Hyderabad',
    'Rajasthan Royals',
    'Punjab Kings'
]

cities = [
    'Mumbai',
    'Delhi',
    'Bangalore',
    'Chennai',
    'Kolkata',
    'Hyderabad'
]

# =========================
# TEAM SELECTION
# =========================

st.markdown(
    "<div class='section'>🏏 Select Teams</div>",
    unsafe_allow_html=True
)

# TEAM SELECTORS
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)


# =========================
# CITY
# =========================

city = st.selectbox("City", cities)

# =========================
# MATCH SITUATION
# =========================

st.markdown(
    "<div class='section'>📊 Match Situation</div>",
    unsafe_allow_html=True
)

# ROW 1
col1, col2 = st.columns(2)

with col1:
    runs_left = st.number_input("Runs Left", min_value=0)

with col2:
    balls_left = st.number_input("Balls Left", min_value=0)

# ROW 2
col3, col4 = st.columns(2)

with col3:
    wickets_left = st.number_input(
        "Wickets Left",
        min_value=0,
        max_value=10
    )

with col4:
    crr = st.number_input(
        "Current Run Rate",
        min_value=0.0
    )

# ROW 3
rrr = st.number_input(
    "Required Run Rate",
    min_value=0.0
)

# =========================
# VALIDATION
# =========================
if batting_team == bowling_team:
    st.warning("⚠️ Teams must be different")

# =========================
# ENCODING
# =========================
team_map = {team: i for i, team in enumerate(teams)}
city_map = {city: i for i, city in enumerate(cities)}

# =========================
# PREDICT
# =========================
if st.button("🎯 Predict Win Probability"):

    input_df = pd.DataFrame([[
        team_map[batting_team],
        team_map[bowling_team],
        city_map[city],
        runs_left,
        balls_left,
        wickets_left,
        crr,
        rrr
    ]], columns=[
        'batting_team',
        'bowling_team',
        'city',
        'runs_left',
        'balls_left',
        'wickets_left',
        'crr',
        'rrr'
    ])

    prob = model.predict_proba(input_df)[0][1]
    win_prob = round(prob * 100, 2)

    st.markdown(
        f"<div class='result'>🏆 Win Probability: {win_prob}%</div>",
        unsafe_allow_html=True
    )

    st.progress(int(win_prob))

    if win_prob > 50:
        st.success("🔥 Batting team likely to WIN")
    else:
        st.error("⚡ Bowling team likely to WIN")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>IPL Analytics Dashboard | Internship Project</p>",
    unsafe_allow_html=True
)