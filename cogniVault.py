import streamlit as st
import json
import hashlib
import csv
from io import StringIO, BytesIO
from fpdf import FPDF

# ----------- Utility functions ------------

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_profiles():
    try:
        with open("profiles.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_profiles(profiles):
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=4)

def export_csv(profile):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Category", "Field", "Value"])
    # Big 5
    for trait, val in profile["big5"].items():
        writer.writerow(["Big 5", trait.capitalize(), val])
    # MBTI
    writer.writerow(["MBTI", "Type", profile["mbti"]])
    # Habits
    for habit, val in profile["habits"].items():
        if isinstance(val, list):
            val = ", ".join(val)
        writer.writerow(["Habits", habit.capitalize(), val])
    # Goals & Motivation
    writer.writerow(["Goals", "Top 3 Goals", profile["goals"]])
    writer.writerow(["Motivation", "Daily Motivation", profile["motivation"]])
    # Memories
    for i, mem in enumerate(profile["memories"], start=1):
        writer.writerow(["Memories", f"Memory {i}", mem])

    return output.getvalue().encode('utf-8')

def export_pdf(profile_data, file_name = 'profile.pdf'):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica","B",16)
    pdf.cell(200,40,"Profile Report", ln=1)

    for key, value in profile_data.items():
        pdf.cell(200,10, f'{key}: {value}', ln=1)

    pdf.output(file_name)
    return file_name


# ----------- Main app ------------

st.title("🧠 NeuroMirror: Build Your Self Profile")

profiles = load_profiles()

# --- Sidebar for login/signup ---
st.sidebar.header("Login / Register")

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if username in profiles and profiles[username]["hashed_pass"] == hash_pass(password):
        st.session_state["current_user"] = username
        st.sidebar.success(f"Logged in as {username}")
    else:
        st.sidebar.error("Invalid username or password")

if st.sidebar.button("Signup"):
    if username in profiles:
        st.sidebar.error("Username already exists")
    elif not username or not password:
        st.sidebar.error("Please enter username and password")
    else:
        profiles[username] = {"hashed_pass": hash_pass(password), "profile_data": {}}
        save_profiles(profiles)
        st.sidebar.success("Signup successful! Please login.")

if st.session_state["current_user"] is None:
    st.info("Please login or signup from the sidebar to start building your profile.")
    st.stop()

user_profile = profiles[st.session_state["current_user"]].get("profile_data", {})

# --- Load saved profile data if exists ---
def get_val(category, key, default):
    try:
        if category == "big5":
            return user_profile.get("big5", {}).get(key, default)
        if category == "habits":
            return user_profile.get("habits", {}).get(key, default)
        if category == "memories":
            mems = user_profile.get("memories", [])
            if key < len(mems):
                return mems[key]
            return default
        if category == "goals":
            return user_profile.get("goals", default)
        if category == "motivation":
            return user_profile.get("motivation", default)
        if category == "mbti":
            return user_profile.get("mbti", default)
    except Exception:
        return default

# --- Form to enter profile info ---
with st.form("profile_form"):

    st.header("Personality Traits (Big 5)")
    openness = st.slider("Openness", 0, 100, get_val("big5", "openness", 50))
    conscientiousness = st.slider("Conscientiousness", 0, 100, get_val("big5", "conscientiousness", 50))
    extraversion = st.slider("Extraversion", 0, 100, get_val("big5", "extraversion", 50))
    agreeableness = st.slider("Agreeableness", 0, 100, get_val("big5", "agreeableness", 50))
    neuroticism = st.slider("Neuroticism", 0, 100, get_val("big5", "neuroticism", 50))

    mbti = st.selectbox("MBTI Type", [
        "INTJ","INTP","ENTJ","ENTP",
        "INFJ","INFP","ENFJ","ENFP",
        "ISTJ","ISFJ","ESTJ","ESFJ",
        "ISTP","ISFP","ESTP","ESFP"
    ], index= [
        "INTJ","INTP","ENTJ","ENTP",
        "INFJ","INFP","ENFJ","ENFP",
        "ISTJ","ISFJ","ESTJ","ESFJ",
        "ISTP","ISFP","ESTP","ESFP"
    ].index(get_val("mbti", None, "INTJ")))

    st.header("Daily Habits")
    exercise = st.checkbox("Exercise regularly", get_val("habits", "exercise", False))
    meditate = st.checkbox("Meditate", get_val("habits", "meditate", False))
    read = st.checkbox("Read books", get_val("habits", "read", False))
    socialize = st.checkbox("Socialize", get_val("habits", "socialize", False))
    other_habits = st.text_input("Other habits (comma separated)", ", ".join(get_val("habits", "other", [])))

    st.header("Goals & Motivations")
    goals = st.text_area("Top 3 goals", get_val("goals", None, ""))
    motivation = st.text_area("What motivates you daily?", get_val("motivation", None, ""))

    st.header("Core Memories or Life Events")
    memory1 = st.text_input("Memory/Event 1", get_val("memories", 0, ""))
    memory2 = st.text_input("Memory/Event 2", get_val("memories", 1, ""))
    memory3 = st.text_input("Memory/Event 3", get_val("memories", 2, ""))

    submitted = st.form_submit_button("Save Profile")

if submitted:
    new_profile = {
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
    profiles[st.session_state["current_user"]]["profile_data"] = new_profile
    save_profiles(profiles)
    st.success("Profile saved successfully!")

# --- Buttons to load or export ---

st.markdown("---")

if st.button("Load My Profile"):
    if "profile_data" in profiles[st.session_state["current_user"]]:
        st.experimental_rerun()  # just reload the page to populate from saved profile
    else:
        st.warning("No saved profile found.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Export to CSV"):
        csv_bytes = export_csv(profiles[st.session_state["current_user"]].get("profile_data", {}))
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"{st.session_state['current_user']}_profile.csv",
            mime="text/csv"
        )

with col2:
    if st.button("Export to PDF"):
        if st.session_state["current_user"] in profiles:
            profile_data = profiles[st.session_state["current_user"]].get("profile_data", {})

            #Generate PDF
            file_name = export_pdf(profile_data)

            #Provide for Download
            with open(file_name,"rb") as f:
                st.download_button("Download PDF", f, "profile.pdf")
        else:
            st.error("Profile not found")
