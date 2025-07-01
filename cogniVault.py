# cogniVault App with Multiple User Registration, Admin Panel, and Profile Picture Saving

import streamlit as st
import json
import hashlib
import csv
from io import StringIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth
import os
import datetime
import openai
import bcrypt

# --------- API Key ---------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------- File Utility Functions ---------
def load_profiles():
    try:
        with open("profiles.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_profiles(profiles):
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=4)

def load_credentials():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"usernames": {}}

def save_credentials(creds):
    with open("users.json", "w") as f:
        json.dump(creds, f, indent=4)

# --------- Session Setup ---------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# --------- Registration (Only for first load) ---------
if not st.session_state.authenticated or not st.session_state.username:
    st.title("Welcome to cogniVault")
    st.subheader("New User Registration")

    credentials = load_credentials()

    new_username = st.text_input("New Username")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if new_username in credentials["usernames"]:
            st.warning("Username already exists.")
        elif not new_username or not new_password:
            st.warning("Please provide both username and password.")
        else:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            credentials["usernames"][new_username] = {
                "name": new_name or new_username,
                "password": hashed_pw
            }
            save_credentials(credentials)
            st.session_state.authenticated = True
            st.session_state.username = new_username
            st.success("✅ Registration successful! You can now continue.")
            st.info("Please manually refresh the page to load your profile.")
    st.stop()

# --------- Authenticated Content ---------
username = st.session_state.username
if not username:
    st.error("User not authenticated.")
    st.stop()

profiles = load_profiles()
user_profile = profiles.get(username, {}).get("profile_data", {})

img_dir = "profile_pics"
os.makedirs(img_dir, exist_ok=True)
profile_picture = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
if profile_picture:
    for ext in [".jpg", ".jpeg", ".png"]:
        old_path = os.path.join(img_dir, f"{username}{ext}")
        if os.path.exists(old_path):
            os.remove(old_path)
    ext = os.path.splitext(profile_picture.name)[1]
    img_path = os.path.join(img_dir, f"{username}{ext}")
    with open(img_path, "wb") as f:
        f.write(profile_picture.read())
    st.session_state["img_path"] = img_path
    st.sidebar.success("Profile picture saved.")

if "img_path" in st.session_state and os.path.exists(st.session_state["img_path"]):
    st.sidebar.image(st.session_state["img_path"], width=150, caption=f"{username}'s Profile Pic")
else:
    for ext in [".jpg", ".jpeg", ".png"]:
        candidate = os.path.join(img_dir, f"{username}{ext}")
        if os.path.exists(candidate):
            st.sidebar.image(candidate, width=150, caption=f"{username}'s Profile Pic")
            break

st.title("cogniVault : Build Your Self Profile")
st.subheader("Big 5 Personality Traits")
big5 = user_profile.get("big5", {
    "openness": 50,
    "conscientiousness": 50,
    "extraversion": 50,
    "agreeableness": 50,
    "neuroticism": 50
})

for trait in big5:
    big5[trait] = st.slider(trait.capitalize(), 0, 100, big5[trait])

if st.button("Save Profile"):
    profiles[username] = {"profile_data": {"big5": big5}}
    save_profiles(profiles)
    st.success("Profile saved successfully.")

fig, ax = plt.subplots()
ax.barh(list(big5.keys()), list(big5.values()))
ax.set_xlabel("Score")
ax.set_ylabel("Traits")
st.pyplot(fig)

def export_csv(profile):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Category", "Field", "Value"])
    for trait, val in profile.get("big5", {}).items():
        writer.writerow(["Big 5", trait.capitalize(), val])
    return output.getvalue().encode('utf-8')

def export_pdf(profile_data, file_name='profile.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 40, "Profile Report", ln=1)
    for key, value in profile_data.items():
        if isinstance(value, dict):
            for k, v in value.items():
                pdf.cell(200, 10, f'{k}: {v}', ln=1)
        else:
            pdf.cell(200, 10, f'{key}: {value}', ln=1)
    pdf.output(file_name)
    return file_name

col1, col2 = st.columns(2)
with col1:
    if st.button("Export to CSV"):
        csv_bytes = export_csv(profiles[username].get("profile_data", {}))
        st.download_button("Download CSV", data=csv_bytes, file_name=f"{username}_profile.csv", mime="text/csv")

with col2:
    if st.button("Export to PDF"):
        pdf_file = export_pdf(profiles[username].get("profile_data", {}))
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, "profile.pdf")

st.header("Talk to your simulated self")

profile_data = profiles.get(username, {}).get("profile_data", {})
user_msg = st.text_input("Ask your simulated self something")
simulate_ideal = st.checkbox("Talk to your *Ideal Self* version")

if user_msg and profile_data:
    if simulate_ideal:
        prompt = f"""You are an ideal version of the user. Their current personality is:
Big 5 Traits: {profile_data.get('big5', {})}
MBTI Type: {profile_data.get('mbti', '')}
Habits: {profile_data.get('habits', {})}
Goals: {profile_data.get('goals', '')}
Motivation: {profile_data.get('motivation', '')}

You have achieved their goals. Based on that, answer this:
\"{user_msg}\"
"""
    else:
        prompt = f"""You are a simulation of the user with the following personality:
Big 5 Traits: {profile_data.get('big5', {})}
MBTI Type: {profile_data.get('mbti', '')}
Habits: {profile_data.get('habits', {})}
Goals: {profile_data.get('goals', '')}
Motivation: {profile_data.get('motivation', '')}
Memories: {profile_data.get('memories', [])}

Now answer this question in their voice:
\"{user_msg}\"
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a digital twin of the user, answering in their voice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        response_text = completion.choices[0].message["content"]

    except openai.error.OpenAIError as e:
        response_text = f"OpenAI API Error: {e.__class__.__name__} - {str(e)}"
    except Exception as e:
        response_text = f"Unknown Error: {type(e).__name__} - {str(e)}"

    st.markdown("### 🧠 Simulated Response")
    st.write(response_text)


