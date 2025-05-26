import streamlit as st
import pickle
import pandas as pd

# Page config
st.set_page_config(page_title="🔥 IPL Win Predictor 🔥", layout='wide')

# Background image URL
BACKGROUND_IMAGE = "https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78b238b5-2310-4870-96c1-f3ef3bd813e4_1024x768.jpeg"

# CSS for full background cover, no repeat, fixed position
st.markdown(
    f"""
    <style>
    /* Make sure html and body take full height */
    html, body, .main {{
        height: 100%;
        margin: 0;
        padding: 0;
    }}
    /* Background image covers full viewport, no repeat */
    .main {{
        background-image: url("{BACKGROUND_IMAGE}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Teams and Cities
teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

# Load model (your local path)
with open(r'C:\Users\balas\OneDrive\Desktop\Balu\Myprojects\vs\iplwinner\pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

# Your app UI now — keep it simple for now
st.title("🔥 IPL Win Predictor 🏆")
st.write("Predict the winning chances of your favorite IPL teams!")

batting_team = st.selectbox('⚔️ Select Batting Team', sorted(teams))
bowling_team = st.selectbox('🛡️ Select Bowling Team', sorted(teams))
selected_city = st.selectbox('🏟️ Select Host City', sorted(cities))
target = st.number_input('🎯 Target Score', min_value=0, step=1)

score = st.number_input('🏏 Current Score', min_value=0, step=1)
overs = st.number_input('⏱️ Overs Completed', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
wickets = st.number_input('⚰️ Wickets Lost', min_value=0, max_value=10, step=1)

if st.button('🔮 Predict Probability'):
    if overs == 0:
        st.warning("Overs can't be zero, bro.")
    elif score > target:
        st.warning("Score can't beat the target yet!")
    else:
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        loss, win = result[0][0], result[0][1]

        st.markdown(f"""
            ### Scorecard
            **Batting Team:** {batting_team}  
            **Bowling Team:** {bowling_team}  
            **Host City:** {selected_city}  
            **Target Score:** {target}  
            **Current Score:** {score} / {wickets}  
            **Overs Completed:** {overs}  
            **Runs Left:** {runs_left}  
            **Balls Left:** {balls_left}  
            **Wickets Remaining:** {wickets_left}  
            **Current Run Rate (CRR):** {crr:.2f}  
            **Required Run Rate (RRR):** {rrr:.2f}  
            ---
            ### Winning Probability
            **{batting_team}:** {round(win * 100)}%  
            **{bowling_team}:** {round(loss * 100)}%  
        """)
else:
    st.info("Fill in the details above and hit **Predict Probability** to see who’s winning! 🚀")
