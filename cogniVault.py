import streamlit as st
import json

def save_user_data(data):
    with open("user_profile.json", "w") as f:
        json.dump(data, f)

st.title(" NeuroMirror: Build Your Self Profile")

st.header("Personality Traits (Big 5)")
openness = st.slider("Openness", 0, 100, 50)
conscientiousness = st.slider("Conscientiousness", 0, 100, 50)
extraversion = st.slider("Extraversion", 0, 100, 50)
agreeableness = st.slider("Agreeableness", 0, 100, 50)
neuroticism = st.slider("Neuroticism", 0, 100, 50)

mbti = st.selectbox("MBTI Type", [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
])

st.header("Daily Habits")
exercise = st.checkbox("Exercise regularly")
meditate = st.checkbox("Meditate")
read = st.checkbox("Read books")
socialize = st.checkbox("Socialize")
other_habits = st.text_input("Other habits (comma separated)")

st.header("Goals & Motivations")
goals = st.text_area("Top 3 goals")
motivation = st.text_area("What motivates you daily?")

st.header("Core Memories or Life Events")
memory1 = st.text_input("Memory/Event 1")
memory2 = st.text_input("Memory/Event 2")
memory3 = st.text_input("Memory/Event 3")

if st.button("Save Profile"):
    user_profile = {
        "big5": {
            "openness": openness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "agreeableness": agreeableness,
            "neuroticism": neuroticism
        },
        "mbti": mbti,
        "habits": {
            "exercise": exercise,
            "meditate": meditate,
            "read": read,
            "socialize": socialize,
            "other": [h.strip() for h in other_habits.split(",")] if other_habits else []
        },
        "goals": goals,
        "motivation": motivation,
        "memories": [memory1, memory2, memory3]
    }
    save_user_data(user_profile)
    st.success("Profile saved successfully!")
