import streamlit as st
import joblib
import pickle
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

# Load Random Forest model and encoders
clf = joblib.load("EDA/ipl_random_forest.joblib")  # ✅ changed from xgboost to random forest
categorical_cols = ['batting_team', 'bowling_team', 'venue', 'toss_winner', 'toss_decision']
encoders = {col: pickle.load(open(f'EDA/label_encoder_{col}.pkl', 'rb')) for col in categorical_cols}

# Constants
TEAMS = [
    'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders',
    'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
    'Royal Challengers Bengaluru', 'Sunrisers Hyderabad'
]

VENUES = [
    'Arun Jaitley Stadium, Delhi', 'Barabati Stadium, Cuttack', 'Barsapara Cricket Stadium, Guwahati',
    'Brabourne Stadium, Mumbai', 'Dr DY Patil Sports Academy, Mumbai',
    'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam',
    'Eden Gardens, Kolkata', 'Ekana Cricket Stadium, Lucknow',
    'Feroz Shah Kotla Ground, Delhi', 'Green Park, Kanpur', 'Holkar Cricket Stadium, Indore',
    'Himachal Pradesh Cricket Association Stadium, Dharamsala', 'JSCA International Stadium Complex, Ranchi',
    'MA Chidambaram Stadium, Chennai', 'Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur',
    'Maharashtra Cricket Association Stadium, Pune', 'M. Chinnaswamy Stadium, Bengaluru',
    'Narendra Modi Stadium, Ahmedabad', 'Punjab Cricket Association IS Bindra Stadium, Mohali',
    'Rajiv Gandhi International Stadium, Hyderabad', 'Sardar Patel Stadium (Motera), Ahmedabad',
    'Saurashtra Cricket Association Stadium, Rajkot', 'Shaheed Veer Narayan Singh International Stadium, Raipur',
    'Sawai Mansingh Stadium, Jaipur', 'Subrata Roy Sahara Stadium, Pune',
    'Vidarbha Cricket Association Stadium, Nagpur', 'Nehru Stadium, Indore'
]

# Page config and background
st.set_page_config(page_title="IPL Match Predictor", page_icon="🏏", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/c/cc/Ipl-2021-ix7zwgff29ylomuf.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)


def overs_to_float(x):
    o, b = str(x).split('.')
    return int(o) + int(b)/6


def get_commentary_tone(wickets_left, overs_left, runs_left, required_run_rate, run_rate):
    if runs_left <= 12 and wickets_left > 5 and required_run_rate <= run_rate:
        return "comfortable"
    elif wickets_left <= 2 or (runs_left > 18 and required_run_rate > run_rate):
        return "nervous"
    elif overs_left < 1 or abs(required_run_rate - run_rate) < 0.5:
        return "thrilling"
    else:
        return "balanced"


def generate_groq_commentary(batting_team, bowling_team, current_score, target_runs, rr, crr, wickets_left, overs_left, venue, predicted_winner):
    runs_left = target_runs - current_score
    overs_left_float = float(str(overs_left).replace(",", "."))
    tone = get_commentary_tone(wickets_left, overs_left_float, runs_left, rr, crr)

    tone_instructions = {
        "comfortable": "Give a calm, confident, maybe slightly celebratory commentary.",
        "nervous": "Make it tense and dramatic. Emphasize pressure, wickets, or tough chase.",
        "thrilling": "Make it highly suspenseful and exciting.",
        "balanced": "Neutral but lively, acknowledging chances for both sides."
    }

    prompt = (
        f"The match is at {venue}. {batting_team} are chasing {target_runs} runs and are currently at {current_score} runs, "
        f"with {wickets_left} wickets in hand and {overs_left} overs left. The required run rate is {rr}, and the current run rate is {crr}. "
        f"As a cricket commentator, {tone_instructions[tone]} "
        f"You predict {predicted_winner} may win but keep it open. Only talk about IPL cricket. "
        f"Write a short IPL-style commentary paragraph and end with a hook line."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert IPL cricket commentator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.95,
        "max_tokens": 300,
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=45)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "⚠️ Failed to generate commentary. Please check your API key or usage limit."
    except Exception as e:
        return f"⚠️ Commentary generation failed: {e}"


# UI Form
st.title("🏏 IPL Match Winner Predictor")
st.markdown("#### Fill in the match details:")

with st.form("ipl_form"):
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox("Batting Team", TEAMS)
        bowling_team = st.selectbox("Bowling Team", [t for t in TEAMS if t != batting_team])
        venue = st.selectbox("Venue", VENUES)
    with col2:
        toss_winner = st.selectbox("Toss Winner", TEAMS)
        toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
        remaining_overs = st.text_input("Overs Left (e.g. 2.3)", value="2.3")
        wickets_left = st.slider("Wickets Left", 1, 10, 3)
        current_score = st.number_input("Current Score", min_value=0, value=150)
        target_runs = st.number_input("Target Score", min_value=1, value=180)

    try:
        overs_float = overs_to_float(remaining_overs)
        overs_faced = 20 - overs_float
        run_rate = round(current_score / overs_faced, 2) if overs_faced > 0 else 0
        runs_left = target_runs - current_score
        required_run_rate = round(runs_left / overs_float, 2) if overs_float > 0 else 0
    except:
        run_rate = required_run_rate = 0

    st.write(f"**Current Run Rate:** {run_rate} | **Required Run Rate:** {required_run_rate}")
    submitted = st.form_submit_button("Predict Winner")

if submitted:
    try:
        features = [
            encoders['batting_team'].transform([batting_team])[0],
            encoders['bowling_team'].transform([bowling_team])[0],
            encoders['venue'].transform([venue])[0],
            encoders['toss_winner'].transform([toss_winner])[0],
            encoders['toss_decision'].transform([toss_decision])[0],
            overs_float,
            wickets_left,
            run_rate,
            required_run_rate
        ]
        pred = clf.predict([features])[0]
        predicted_winner = bowling_team if pred == 0 else batting_team
        st.markdown(f"<h2 style='text-align:center;color:#FFD700;'>🏆 Predicted Winner: <span style='color:#00FFFF'>{predicted_winner}</span></h2>", unsafe_allow_html=True)
        st.balloons()
    except Exception as e:
        st.error(f"Prediction Error: {e}")
        st.stop()

    with st.spinner("🎙️ Generating Live Commentary..."):
        commentary = generate_groq_commentary(
            batting_team, bowling_team, current_score, target_runs,
            required_run_rate, run_rate, wickets_left, remaining_overs,
            venue, predicted_winner
        )

    st.subheader("🎤 Live Commentary")
    st.markdown(
        f"""
        <div style="
            background: #0d1b2a;
            color: #FFD700;
            border-radius: 15px;
            padding: 25px;
            font-size: 1.1rem;
            text-align: center;
            line-height: 1.8;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        ">
        {commentary}
        </div>
        """, unsafe_allow_html=True
    )
