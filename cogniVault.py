# cogniVault App with Multiple User Registration, Admin Panel, and Profile Picture Saving

import streamlit as st
import json
import hashlib
<<<<<<< HEAD
import bcrypt
import os
import openai
from datetime import datetime
import requests
import speech_recognition as sr
import matplotlib as plt
from cryptography.fernet import Fernet
from collections import Counter
import matplotlib.pyplot as plt





# --------- DEV MODE ---------
dev_mode = False
default_dev_user = "devuser"

# --------- Encryption Setup ---------
ENCRYPTION_KEY = os.environ.get("SESSION_ENCRYPT_KEY") or Fernet.generate_key().decode()
fernet = Fernet(ENCRYPTION_KEY.encode())

# --------- Session Memory ---------
def save_session_state():
    session_data = json.dumps({
        "remembered_username": st.session_state.get("remembered_username", ""),
        "remembered_password": st.session_state.get("remembered_password", ""),
        "remember_me": st.session_state.get("remember_me", False)
    })
    encrypted_data = fernet.encrypt(session_data.encode()).decode()
    with open("session.json", "w") as f:
        f.write(encrypted_data)

def load_session_state():
    try:
        with open("session.json", "r") as f:
            encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
            data = json.loads(decrypted_data)
            st.session_state["remembered_username"] = data.get("remembered_username", "")
            st.session_state["remembered_password"] = data.get("remembered_password", "")
            st.session_state["remember_me"] = data.get("remember_me", False)
    except:
        st.session_state["remembered_username"] = ""
        st.session_state["remembered_password"] = ""
        st.session_state["remember_me"] = False

load_session_state()

# --------- API Setup ---------
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["openrouter_api_key"]
)

# --------- File Utilities ---------
def load_credentials():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"usernames": {}}

def save_credentials(creds):
    with open("users.json", "w") as f:
        json.dump(creds, f, indent=4)
=======
import csv
from io import StringIO
from fpdf import FPDF

# Fix matplotlib import for environments without it
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    import os
    os.system("pip install matplotlib")
    import matplotlib.pyplot as plt

import streamlit_authenticator as stauth
import datetime
import openai
import bcrypt
>>>>>>> e404ebc657dd34560f6155b0ae034a0fd306a657

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

<<<<<<< HEAD
def load_goals(username):
    path = f"chat_logs/{username}/goals.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_goals(username, goals):
    os.makedirs(f"chat_logs/{username}", exist_ok=True)
    with open(f"chat_logs/{username}/goals.json", "w") as f:
        json.dump(goals, f, indent=4)

def get_memory_count_per_goal(memory_logs, goals):
    goal_counts = {goal["title"]: 0 for goal in goals}
    for mem in memory_logs:
        for goal in mem.get("linked_goals", []):
            if goal in goal_counts:
                goal_counts[goal] += 1
    return goal_counts


def generate_goal_insight(goal, memory_logs, api_key):
    linked_memories = [
        mem["text"] for mem in memory_logs
        if goal["title"] in mem.get("linked_goals", [])
    ]
    if not linked_memories:
        return "No reflections linked yet for insight generation."

    prompt = (
        f"You are a reflective thought partner. Analyze the following memories linked to the user's goal "
        f"'{goal['title']}' and summarize their progress, mindset patterns, and suggestions for improvement:\n\n"
        f"Memories:\n- " + "\n- ".join(linked_memories)
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openrouter/auto",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Insight generation failed: {e}"



def load_chat_sessions(username):
    os.makedirs(f"chat_logs/{username}", exist_ok=True)
    return sorted([f[:-5] for f in os.listdir(f"chat_logs/{username}") if f.endswith(".json")])

def load_chat_history(username, session_id):
    path = f"chat_logs/{username}/{session_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_chat_history(username, session_id, history):
    os.makedirs(f"chat_logs/{username}", exist_ok=True)
    with open(f"chat_logs/{username}/{session_id}.json", "w") as f:
        json.dump(history, f, indent=4)
def generate_session_summary(chat_history):
    prompt = f"""Summarize the following chat in 3-5 bullet points. Highlight emotional tone, cognitive patterns, and intent. Then tag the session with keywords like Reflective, Curious, Motivated, etc.

Chat History:
{json.dumps(chat_history, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You summarize and analyze user conversations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Summary generation failed: {e}"

def save_summary(username, session_id, summary_text):
    with open(f"chat_logs/{username}/summary_{session_id}.txt", "w") as f:
        f.write(summary_text)

def load_summary(username, session_id):
    path = f"chat_logs/{username}/summary_{session_id}.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def load_recent_summaries(username, exclude_session_id=None, limit=3):
    summaries = []
    sessions = sorted([
        s for s in os.listdir(f"chat_logs/{username}")
        if s.startswith("summary_") and s.endswith(".txt") and (exclude_session_id not in s)
    ], reverse=True)
    for sfile in sessions[:limit]:
        with open(f"chat_logs/{username}/{sfile}", "r") as f:
            summaries.append(f.read())
    return summaries

# --------- Day 20: Memory Persistence Utilities ---------
def save_memory_logs(username, memory_logs):
    os.makedirs(f"chat_logs/{username}", exist_ok=True)
    with open(f"chat_logs/{username}/memories_{username}.json", "w") as f:
        json.dump(memory_logs, f, indent=4)

def load_memory_logs(username):
    path = f"chat_logs/{username}/memories_{username}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# --------- Day 23: Memory Tag Insight Generation ---------
def generate_tag_insight(tag, memories, client):

    prompt = f"""You are an introspective AI helping a user understand their emotional and cognitive patterns.

Analyze the following memories tagged with "{tag}". Summarize any patterns, recurring themes, or insights that emerge. Keep it to 2-3 sentences.

Memories:
{json.dumps(memories, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You analyze grouped memories and provide emotional/cognitive insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate insight for {tag}: {e}"

def generate_memory_insights(memories, client):
    prompt = f"""
You are an introspective AI analyzing a user's memory logs.

1. Summarize recurring emotional or cognitive patterns.
2. Identify any correlations between emotion and cognition tags.
3. Provide a short personal insight (2–3 sentences).
4. Report memory activity level (weekly volume or spike).

Memories:
{json.dumps(memories, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You analyze and summarize memory patterns for insight."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate memory insights: {e}"
    
def generate_persona_reflection(memory_text, persona_name, client):
    persona_prompts = {
        "Coach": "Motivational and direct. Focus on growth and discipline.",
        "Mentor": "Wise and experienced. Reflect with calm, strategic advice.",
        "Friend": "Supportive and caring. Provide emotional encouragement.",
        "Inner Critic": "Blunt and skeptical. Question weaknesses.",
    }
    
    persona_style = persona_prompts.get(persona_name, "Provide thoughtful reflection.")
    
    prompt = f"""
You are the user's {persona_name}.
Style: {persona_style}

Reflect on this memory in 2-3 sentences:
\"\"\"{memory_text}\"\"\"
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a {persona_name} giving perspective."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"{persona_name} reflection failed: {e}"
    
def analyze_growth_trends(memories, client):
    prompt = f"""
You are an AI mentor helping a user track emotional and cognitive growth.

Analyze these memory logs and identify:
1. Key emotional trends over time (what’s increasing/decreasing).
2. Major cognitive shifts.
3. Any breakthroughs or milestone changes.
Respond in 4–5 bullet points.

Memories:
{json.dumps(memories, indent=2)}
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You summarize personal growth trends from memories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Growth analysis failed: {e}"




# --------- Day 25: Threaded Reflection Generator ---------
def generate_reflection_thread(memory, all_memories):
    prompt = f"""
You are the user's reflective AI. Expand upon the memory below into a 3-step cognitive reflection chain.

1. Restate and elaborate the memory.
2. Reflect on what it might mean emotionally or psychologically.
3. Suggest how this could impact future decisions or mindset.

Memory: {memory.get('text')}
Context:
{json.dumps(all_memories, indent=2)}
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You generate threaded reflections for personal memories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Reflection generation failed: {e}"
    # --------- Day 27: Theme and Label Detection ---------
def detect_memory_theme_and_label(memory_text):
    prompt = f"""
You are an intelligent cognitive assistant. Analyze the following personal memory and identify:

1. The high-level **theme** (like Work, Health, Self-Reflection, Relationships, Emotions, Goals, etc.)
2. The **label** (choose one: Growth Moment, Setback, Breakthrough, Insight, Conflict, Success)

Memory:
\"\"\"{memory_text}\"\"\"

Respond in JSON like:
{{
  "theme": "Self-Reflection",
  "label": "Insight"
}}
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You extract themes and emotional labels from personal reflections."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        data = json.loads(response.choices[0].message.content)
        return data.get("theme", ""), data.get("label", "")
    except Exception as e:
        return "Unknown", "Unlabeled"



# --------- Session Init ---------
def init_session():
    defaults = {
        "authenticated": False,
        "username": None,
        "profile_complete": False,
        "chat_history": [],
        "chat_session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "theme": "light",
        "failed_attempts": 0,
        "search_term": "",
        "selected_role": "Default",
        "voice_input": "",
        "remember_me": st.session_state.get("remember_me", False),
        "remembered_username": st.session_state.get("remembered_username", ""),
        "remembered_password": st.session_state.get("remembered_password", ""),
        "chat_input": "",
        "search_history": "",
        "chat_error": "",
        "show_memory_popup": False,
        "show_goal_popup": False,
        "show_customizer": False  # Day 24 – AI customization toggle
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()
if st.session_state.authenticated:
    save_session_state()
# --------- Login/Register ---------
if dev_mode:
    st.session_state.authenticated = True
    st.session_state.username = default_dev_user

if not st.session_state.authenticated:
    st.title("Welcome to CogniVault")
    mode = st.radio("Select", ["Login", "Register"])
    username = st.text_input("Username", value=st.session_state.get("remembered_username", ""))
    password = st.text_input("Password", type="password", value=st.session_state.get("remembered_password", ""))
    st.session_state.remember_me = st.checkbox("Remember me", value=st.session_state.get("remember_me", False))
    credentials = load_credentials()

    if mode == "Login":
        if st.button("Login"):
            if username in credentials["usernames"] and bcrypt.checkpw(password.encode(), credentials["usernames"][username]["password"].encode()):
                st.session_state.authenticated = True
                st.session_state.username = username
                if st.session_state.remember_me:
                    st.session_state.remembered_username = username
                    st.session_state.remembered_password = password
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        name = st.text_input("Full Name")
        if st.button("Register"):
            if username in credentials["usernames"]:
                st.warning("Username exists")
            elif not username or not password:
                st.warning("Please complete all fields")
            else:
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                credentials["usernames"][username] = {"name": name, "password": hashed_pw}
                save_credentials(credentials)
                st.success("Registration successful")
                st.rerun()
    st.stop()

# --------- Profile Setup ---------
profiles = load_profiles()
username = st.session_state.username
profile_data = profiles.get(username, {}).get("profile_data", {})

# --------- Day 20: Load Memory Logs ---------
if "memory_logs" not in st.session_state:
    st.session_state.memory_logs = load_memory_logs(username)

if not profile_data:
    st.title("Build Your Digital Twin")
    with st.form("profile_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=10, max_value=100)
        height = st.text_input("Height")
        mbti = st.selectbox("MBTI Type", [
            "INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
            "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"
        ])
        goals = st.text_area("Your Life Goals")
        habits = st.text_area("Your Daily Habits")
        motivation = st.text_area("What motivates you?")
        memories = st.text_area("List 3 memories that shaped you")
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            profiles[username] = {
                "profile_data": {
                    "name": name, "age": age, "height": height,
                    "mbti": mbti, "goals": goals,
                    "habits": habits, "motivation": motivation,
                    "memories": memories
                }
            }
            save_profiles(profiles)
            st.session_state.profile_complete = True
            st.rerun()
    st.stop()

# --------- Sidebar: Chats, Summaries, Timeline ---------
st.sidebar.markdown("### 💬 Chats")
if st.sidebar.button("➕ New Chat"):
    new_sid = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.chat_session_id = new_sid
    st.session_state.chat_history = []
    st.session_state.chat_input = ""
    st.session_state.voice_input = ""
    st.rerun()

summary_disabled = not st.session_state.get("chat_history")
if st.sidebar.button("🧠 Generate Summary", disabled=summary_disabled):
    summary = generate_session_summary(st.session_state.chat_history)
    save_summary(username, st.session_state.chat_session_id, summary)
    st.session_state.generated_summary = summary
if "generated_summary" in st.session_state:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📝 Session Summary")
    st.sidebar.text_area("Summary", st.session_state.generated_summary, height=200)

# Timeline Display – Day 19 Feature
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Memory Timeline")
recent_summaries = load_recent_summaries(username, exclude_session_id=st.session_state.chat_session_id)
if recent_summaries:
    for i, summ in enumerate(recent_summaries):
        with st.sidebar.expander(f"🧠 Past Memory {i+1}"):
            st.write(summ)
else:
    st.sidebar.info("No prior memories saved.")

# Chat Session Selector
st.sidebar.text_input("Search chat history", key="search_history", placeholder="Search...")
sessions = load_chat_sessions(username)
for sid in sessions:
    if st.session_state.search_history and st.session_state.search_history.lower() not in sid.lower():
        continue
    label = f"📂 {sid[-6:]}"
    if st.sidebar.button(label, key=f"load_{sid}"):
        st.session_state.chat_session_id = sid
        st.session_state.chat_history = load_chat_history(username, sid)
        st.session_state.chat_input = ""
        st.rerun()

# --------- AI Mode Selector + Customization Button ---------
st.sidebar.markdown("---")
col_mode, col_icon = st.sidebar.columns([8, 1])
with col_mode:
    st.session_state.selected_role = st.selectbox("🧠 Choose AI Mode", ["Default", "Ideal Self", "Coach", "Mentor", "Friend"], key="mode_select_sidebar")

with col_icon:
    if st.button("⚙️", key="customize_toggle"):
        st.session_state.toggle_customize_popup = not st.session_state.get("toggle_customize_popup", False)

if st.session_state.get("toggle_customize_popup", False):
    with st.sidebar.expander("🎛 Customize AI Persona", expanded=True):
        tone = st.text_input("Tone (e.g., Empathetic, Direct, Playful)", key="tone_input")
        intent = st.text_input("Intent (e.g., Motivate, Challenge, Guide)", key="intent_input")
        memory_focus = st.text_input("Memory Focus (e.g., Past trauma, Career goals)", key="memory_focus_input")
        st.session_state.customization_settings = {
            "tone": tone,
            "intent": intent,
            "memory_focus": memory_focus
        }
# Add this helper function just above the buttons:
def close_all_popups(except_popup=None):
    keys = ["show_memory_popup", "show_insights_popup", "show_compare_popup", "show_growth_popup"]
    for k in keys:
        st.session_state[k] = (k == except_popup and not st.session_state.get(k, False))

# Replace the buttons section:
col_left, col_mid, col_center, col_right, col_growth, col_goal = st.columns([5.5, 1, 1, 1, 1, 1])
with col_left:
    st.title(f"🤖 Hello {profile_data.get('name', username)}, talk to CogniVault")

with col_mid:
    if st.button("🔍", key="open_mem_popup"):
        close_all_popups("show_memory_popup")

with col_center:
    if st.button("🧠", key="open_insight_popup"):
        close_all_popups("show_insights_popup")

with col_right:
    if st.button("🎭", key="open_compare_popup"):
        close_all_popups("show_compare_popup")

with col_growth:
    if st.button("📈", key="open_growth_popup"):
        close_all_popups("show_growth_popup")

with col_goal:
    if st.button("🎯", key="open_goal_popup"):
        st.session_state.show_goal_popup = not st.session_state.get("show_goal_popup", False)






# --------- Input Field and Voice Input ---------
col1, col2 = st.columns([9, 1])
with col1:
    st.session_state.voice_input = st.text_input(
        "", placeholder="Ask anything...", value=st.session_state.voice_input, label_visibility="collapsed"
    )

    # --------- Voice Status Display (below input box) ---------
    mic_status = st.session_state.get("mic_status", "")
    mic_error = st.session_state.get("mic_error", "")

    if mic_status == "listening":
        st.markdown("""
        <div style="background-color:#007BFF; color:white; padding:10px 16px; border-radius:8px; margin-top:10px; font-weight:bold; width:100%; text-align:left;">
        🎙 Listening...
        </div>
        """, unsafe_allow_html=True)
    elif mic_status == "transcribing":
        st.markdown("""
        <div style="background-color:#17A2B8; color:white; padding:10px 16px; border-radius:8px; margin-top:10px; font-weight:bold; width:100%; text-align:left;">
        📝 Transcribing...
        </div>
        """, unsafe_allow_html=True)
    elif mic_status == "error":
        st.markdown(f"""
        <div style="background-color:#dc3545; color:white; padding:10px 16px; border-radius:8px; margin-top:10px; font-weight:bold; width:100%; text-align:left;">
        ⚠️ Mic error: {mic_error}
        </div>
        """, unsafe_allow_html=True)

with col2:
    mic, send = st.columns([1, 1])
    with mic:
        if st.button("🎤", key="mic_record"):
            recognizer = sr.Recognizer()
            mic_input = sr.Microphone()
            try:
                st.session_state["mic_status"] = "listening"
                st.session_state["mic_error"] = ""
                st.rerun()  # Immediately update UI with listening message

                with mic_input as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)

                st.session_state["mic_status"] = "transcribing"
                st.rerun()  # Update UI to show transcribing

                st.session_state.voice_input = recognizer.recognize_google(audio)
                st.session_state["mic_status"] = ""
                st.rerun()

            except Exception as e:
                st.session_state["mic_status"] = "error"
                st.session_state["mic_error"] = str(e)
                st.rerun()



    with send:
        if st.button("↑", key="send_input"):
            chat_input = st.session_state.voice_input.strip()
            if chat_input:
                st.session_state.chat_history.append({"role": "user", "content": chat_input})
                context = st.session_state.chat_history[-3:]
                memory_summaries = load_recent_summaries(username, exclude_session_id=st.session_state.chat_session_id, limit=3)
                memory_text = "\n\n".join(memory_summaries)
                memory_prefix = f"Previously on CogniVault:\n{memory_text}" if memory_summaries else ""

                persona_details = st.session_state.get("customization_settings", {})
                persona_instruction = f"Use tone: {persona_details.get('tone', 'default')}, intent: {persona_details.get('intent', 'default')}, focus on: {persona_details.get('memory_focus', 'none')}."

                try:
                    system_prompt = {
                        "role": "system",
                        "content": f"""You are the user's cognitive twin. Profile: {profile_data}.
Memory Recall: {memory_prefix}
Persona Mode: {st.session_state.selected_role}
{persona_instruction}
Continue the conversation naturally."""
                    }
                    messages = [system_prompt] + [
                        {"role": m.get("role", "user"), "content": m.get("content", "")}
                        for m in context
                    ]
                    response = client.chat.completions.create(
                        model="openai/gpt-4o",
                        messages=messages,
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    save_chat_history(username, st.session_state.chat_session_id, st.session_state.chat_history)
                    st.session_state.voice_input = ""
                    st.session_state.chat_error = ""
                except Exception as e:
                    st.session_state.chat_error = str(e)
# --------- Error Display ---------
if st.session_state.get("chat_error"):
    err = st.session_state.chat_error
    if "402" in err:
        st.error("🚫 Token limit exceeded on OpenRouter.")
    else:
        st.error(f"⚠️ {err.replace(chr(10), ' ')}")
    st.session_state.chat_error = ""

# --------- Chat Display with Memory Tagging ---------
for i, entry in enumerate(st.session_state.chat_history):
    with st.container():
        role = entry.get("role", "")
        content = entry.get("content", "")
        if role == "user":
            st.markdown(f"<div style='background:#e0e0e0;padding:10px;border-radius:10px;margin:5px 0'><b>You:</b><br>{content}</div>", unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown(f"<div style='background:#d2f8d2;padding:10px;border-radius:10px;margin:5px 0'><b>CogniVault:</b><br>{content}</div>", unsafe_allow_html=True)

        if st.checkbox("⭐ Mark as memory", key=f"mem_{i}"):
            profile_data.setdefault("memories", "")
            profile_data["memories"] += f"\n{content}"
            profiles[username]["profile_data"] = profile_data
            save_profiles(profiles)

# --------- Day 28: Simulated Memory Web ---------
def get_related_memories(current_memory, all_memories, max_links=3):
    related = []
    for mem in all_memories:
        if mem == current_memory:
            continue
        score = 0
        reasons = []

        shared_tags = set(current_memory.get("tags", [])) & set(mem.get("tags", []))
        if shared_tags:
            score += len(shared_tags)
            reasons.append(f"Shared tag(s): {', '.join(shared_tags)}")

        if current_memory.get("theme") and current_memory.get("theme") == mem.get("theme"):
            score += 1
            reasons.append(f"Same theme: {current_memory.get('theme')}")

        if current_memory.get("emotion_tag") and current_memory.get("emotion_tag") == mem.get("emotion_tag"):
            score += 1
            reasons.append(f"Similar emotion: {current_memory.get('emotion_tag')}")

        if score > 0:
            related.append((mem, score, reasons))

    related.sort(key=lambda x: -x[1])
    return related[:max_links]


# --------- Memory Manager Timeline (Day 20–23) ---------
if st.session_state.get("show_memory_popup"):
    with st.expander("🧠 Editable Memory Timeline", expanded=True):
        # --------- Load available goals for linking ---------
        goals_file = f"chat_logs/{username}/goals.json"
        goals = []
        if os.path.exists(goals_file):
            with open(goals_file, "r") as f:
                goals_data = json.load(f)
                goals = [g["title"] for g in goals_data]

        if st.button("❌ Close", key="close_mem_popup"):
            st.session_state.show_memory_popup = False
            st.stop()

        # Day 27 – Group by Theme toggle
        group_by_theme = st.toggle("🧩 Group by Theme View", key="group_by_theme")

        st.markdown("### 🔍 Filter & Search")
        search_query = st.text_input("Search memories...")
        all_emotions = sorted(set(m.get("emotion_tag") for m in st.session_state.memory_logs if m.get("emotion_tag")))
        all_cognitions = sorted(set(m.get("cognitive_tag") for m in st.session_state.memory_logs if m.get("cognitive_tag")))
        selected_emotions = st.multiselect("Filter by Emotion", options=all_emotions)
        selected_cognitions = st.multiselect("Filter by Cognition", options=all_cognitions)

        
        # Default to empty or stored value
        default_start = st.session_state.get("start_date_filter", None)
        default_end = st.session_state.get("end_date_filter", None)

        start_date = st.date_input("Start Date", value=default_start, key="start_date_input")
        end_date = st.date_input("End Date", value=default_end, key="end_date_input")


        if st.button("🔄 Clear Date Filter"):
            st.session_state["start_date_filter"] = None
            st.session_state["end_date_filter"] = None
            st.rerun()


        # Sort Toggle
        sort_toggle = st.radio("🗂 Sort Memories", ["Newest First", "Oldest First"], horizontal=True)

        # FILTERING STARTS HERE
        filtered_memories = st.session_state.memory_logs

        if search_query:
            filtered_memories = [m for m in filtered_memories if
                search_query.lower() in m.get("text", "").lower() or
                search_query.lower() in m.get("emotion_tag", "").lower() or
                search_query.lower() in m.get("cognitive_tag", "").lower()]

        if selected_emotions:
            filtered_memories = [m for m in filtered_memories if m.get("emotion_tag") in selected_emotions]

        if selected_cognitions:
            filtered_memories = [m for m in filtered_memories if m.get("cognitive_tag") in selected_cognitions]

        # ✅ Safely track start and end date in session_state before using them
        st.session_state["start_date_filter"] = start_date
        st.session_state["end_date_filter"] = end_date

        # ✅ Now apply the date filter using those values
        if start_date and end_date:
            filtered_memories = [
                m for m in filtered_memories
                if start_date <= datetime.strptime(m.get("timestamp", ""), "%Y-%m-%d %H:%M:%S").date() <= end_date
            ]


        if sort_toggle == "Newest First":
            filtered_memories.sort(key=lambda m: m.get("timestamp", ""), reverse=True)
        else:
            filtered_memories.sort(key=lambda m: m.get("timestamp", ""))

        # === MEMORY DISPLAY ===
        if group_by_theme:
            st.info("🔒 Add Memory only available in Ungrouped View.\n\nPlease turn off 'Group by Theme' to add new memories.")

            theme_groups = {}
            for m in filtered_memories:
                theme = m.get("theme", "Uncategorized")
                theme_groups.setdefault(theme, []).append(m)

            for theme, mem_group in theme_groups.items():
                with st.expander(f"🏷️ Theme: {theme} ({len(mem_group)})", expanded=False):
                    for idx, memory in enumerate(mem_group):
                        st.markdown("---")
                        st.markdown(f"**🧠 Memory**")
                        st.markdown(f"🧩 Theme: `{memory.get('theme', 'None')}` — 📚 Label: `{memory.get('label', 'None')}`")

                        st.text_input("Memory Text", value=memory.get("text", ""), key=f"mem_text_{theme}_{idx}")
                        st.text_input("Emotion Tag", value=memory.get("emotion_tag", ""), key=f"mem_emotion_{theme}_{idx}")
                        st.text_input("Cognitive Tag", value=memory.get("cognitive_tag", ""), key=f"mem_cognition_{theme}_{idx}")
                        st.text_input("Theme", value=memory.get("theme", ""), key=f"mem_theme_{theme}_{idx}")
                        st.text_input("Label", value=memory.get("label", ""), key=f"mem_label_{theme}_{idx}")

                        if f"show_thread_{theme}_{idx}" not in st.session_state:
                            st.session_state[f"show_thread_{theme}_{idx}"] = False

                        if st.button("🧵 Show/Hide Reflection", key=f"thread_toggle_{theme}_{idx}"):
                            st.session_state[f"show_thread_{theme}_{idx}"] = not st.session_state[f"show_thread_{theme}_{idx}"]

                        if st.session_state[f"show_thread_{theme}_{idx}"]:
                            if not memory.get("threaded_reflection"):
                                memory["threaded_reflection"] = generate_reflection_thread(memory, st.session_state.memory_logs)
                                save_memory_logs(username, st.session_state.memory_logs)
                            st.markdown(memory.get("threaded_reflection", "⚠️ No reflection generated yet."))

                        if st.button("🔁 Regenerate", key=f"regen_thread_{theme}_{idx}"):
                            with st.spinner("Regenerating reflection..."):
                                memory["threaded_reflection"] = generate_reflection_thread(memory, st.session_state.memory_logs)
                                save_memory_logs(username, st.session_state.memory_logs)
                                st.rerun()

                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("💾 Save", key=f"save_mem_{theme}_{idx}"):
                                memory["text"] = st.session_state[f"mem_text_{theme}_{idx}"]
                                memory["emotion_tag"] = st.session_state[f"mem_emotion_{theme}_{idx}"]
                                memory["cognitive_tag"] = st.session_state[f"mem_cognition_{theme}_{idx}"]
                                memory["theme"] = st.session_state[f"mem_theme_{theme}_{idx}"]
                                memory["label"] = st.session_state[f"mem_label_{theme}_{idx}"]
                                save_memory_logs(username, st.session_state.memory_logs)
                                st.rerun()
                        with col2:
                            if st.button("❌ Delete", key=f"del_mem_{theme}_{idx}"):
                                st.session_state.memory_logs.remove(memory)
                                save_memory_logs(username, st.session_state.memory_logs)
                                st.rerun()
        else:
            for idx, memory in enumerate(reversed(filtered_memories)):
                st.markdown("---")
                st.markdown(f"**🧠 Memory #{len(filtered_memories) - idx}**")
                st.markdown(f"🧩 Theme: `{memory.get('theme', 'None')}` — 📚 Label: `{memory.get('label', 'None')}`")

                st.text_input("Memory Text", value=memory.get("text", ""), key=f"mem_text_{idx}")
                st.text_input("Emotion Tag", value=memory.get("emotion_tag", ""), key=f"mem_emotion_{idx}")
                st.text_input("Cognitive Tag", value=memory.get("cognitive_tag", ""), key=f"mem_cognition_{idx}")
                st.text_input("Theme", value=memory.get("theme", ""), key=f"mem_theme_{idx}")
                st.text_input("Label", value=memory.get("label", ""), key=f"mem_label_{idx}")

                if f"show_thread_{idx}" not in st.session_state:
                    st.session_state[f"show_thread_{idx}"] = False

                if st.button("🧵 Show/Hide Reflection", key=f"thread_toggle_{idx}"):
                    st.session_state[f"show_thread_{idx}"] = not st.session_state[f"show_thread_{idx}"]

                if st.session_state[f"show_thread_{idx}"]:
                    if not memory.get("threaded_reflection"):
                        memory["threaded_reflection"] = generate_reflection_thread(memory, st.session_state.memory_logs)
                        save_memory_logs(username, st.session_state.memory_logs)
                    st.markdown(memory.get("threaded_reflection", "⚠️ No reflection generated yet."))

                if st.button("🔁 Regenerate", key=f"regen_thread_{idx}"):
                    with st.spinner("Regenerating reflection..."):
                          memory["threaded_reflection"] = generate_reflection_thread(memory, st.session_state.memory_logs)
                          save_memory_logs(username, st.session_state.memory_logs)
                          st.rerun()

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("💾 Save", key=f"save_mem_{idx}"):
                        memory["text"] = st.session_state[f"mem_text_{idx}"]
                        memory["emotion_tag"] = st.session_state[f"mem_emotion_{idx}"]
                        memory["cognitive_tag"] = st.session_state[f"mem_cognition_{idx}"]
                        memory["theme"] = st.session_state[f"mem_theme_{idx}"]
                        memory["label"] = st.session_state[f"mem_label_{idx}"]
                        save_memory_logs(username, st.session_state.memory_logs)
                        st.rerun()
                with col2:
                    if st.button("❌ Delete", key=f"del_mem_{idx}"):
                        st.session_state.memory_logs.remove(memory)
                        save_memory_logs(username, st.session_state.memory_logs)
                        st.rerun()

                # 🧬 Related Memories
                related_memories = get_related_memories(memory, st.session_state.memory_logs)
                if related_memories:
                    with st.expander("🧬 Memory Connections", expanded=False):
                        for rel_mem, score, reasons in related_memories:
                            st.markdown(f"**Related to:** `{rel_mem['text'][:60]}...`")
                            for reason in reasons:
                                st.markdown(f"- {reason}")
                        st.markdown("---")
        # === 📊 Day 29: Mood Mapping & Cognitive Analytics ===
        with st.container():
            st.subheader("📊 Memory Mood & Analytics")


            # Collect emotion and cognition tags
            emotions = [m.get("emotion_tag", "").strip().lower() for m in st.session_state.memory_logs if m.get("emotion_tag")]
            cognitions = [m.get("cognitive_tag", "").strip().lower() for m in st.session_state.memory_logs if m.get("cognitive_tag")]

            emotion_counts = Counter(emotions)
            cognition_counts = Counter(cognitions)

            # Emotion Frequency Chart
            st.subheader("📈 Emotion Frequency")
            if emotion_counts:
                fig, ax = plt.subplots()
                ax.bar(emotion_counts.keys(), emotion_counts.values())
                ax.set_ylabel("Count")
                ax.set_xlabel("Emotion Tag")
                ax.set_title("Emotion Frequency in Memories")
                plt.xticks(rotation=30)
                st.pyplot(fig)
            else:
                st.info("No emotion tags found yet.")

            # Cognitive Tag Summary
            st.subheader("🧠 Cognitive Tag Stats")
            if cognition_counts:
                for tag, count in cognition_counts.items():
                    st.markdown(f"- **{tag.capitalize()}**: {count}")
            else:
                st.info("No cognitive tags found yet.")


         # --------- Load user goals before the form ---------
goals_file = f"chat_logs/{username}/goals.json"
goals = []
if os.path.exists(goals_file):
    with open(goals_file, "r") as f:
        goals_data = json.load(f)
        goals = [g["title"] for g in goals_data]

# ✅ ➕ Add Memory (outside loop)
st.markdown("### ➕ Add New Memory")
with st.form("add_memory_form"):
    new_mem_text = st.text_input("Memory")
    new_emotion = st.text_input("Emotion Tag")
    new_cognition = st.text_input("Cognitive Tag")

    # ✅ Step 2: Goal linking multiselect
    linked_goals = st.multiselect("🎯 Link to Goal(s)", goals, key="goal_link_selector")

    submitted = st.form_submit_button("Add")

    if submitted and new_mem_text:
        theme, label = detect_memory_theme_and_label(new_mem_text)

        new_memory = {
            "text": new_mem_text,
            "emotion_tag": new_emotion,
            "cognitive_tag": new_cognition,
            "linked_goals": linked_goals,  # ✅ Save linked goals
            "theme": theme,
            "label": label,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        new_memory["threaded_reflection"] = generate_reflection_thread(
            new_memory, st.session_state.memory_logs
        )

        st.session_state.memory_logs.append(new_memory)
        save_memory_logs(username, st.session_state.memory_logs)
        st.rerun()



# --------- Day 23: Tag Cluster Analysis (OUTSIDE the Expander to avoid nesting issue) ---------
if st.session_state.get("show_memory_popup"):
    st.markdown("### 🧠 Clustered Memory Insights")

    tag_clusters = {}
    for mem in st.session_state.memory_logs:
        for tag_type in ["emotion_tag", "cognitive_tag"]:
            tag = mem.get(tag_type)
            if tag:
                tag_clusters.setdefault(tag, []).append(mem)

    for tag, cluster in tag_clusters.items():
       with st.expander(f"🔖 {tag} – {len(cluster)} memory{'ies' if len(cluster) > 1 else ''}", expanded=False):
           for m in cluster:
               st.markdown(f"- {m['text']}")
           if st.button(f"🧠 Analyze '{tag}'", key=f"analyze_{tag}_{len(cluster)}"):
               with st.spinner(f"Analyzing memories tagged with '{tag}'..."):
                   insight = generate_tag_insight(tag, cluster, client)
                   st.success(insight)


# --------- Persona Customizer Modal (Day 24) ---------
if st.session_state.get("show_customizer"):
    st.markdown("---")
    st.markdown("### 🎨 AI Persona Customization")
    with st.form("persona_customizer_form"):
        role = st.text_input("Role (e.g., Therapist, Coach, Best Friend)", value=st.session_state.get("persona_role", ""))
        tone = st.text_input("Tone (e.g., Empathetic, Encouraging)", value=st.session_state.get("persona_tone", ""))
        intent = st.text_area("Intent (What this AI persona aims to do)", value=st.session_state.get("persona_intent", ""))
        submitted = st.form_submit_button("Save Persona")
        if submitted:
            st.session_state.persona_role = role
            st.session_state.persona_tone = tone
            st.session_state.persona_intent = intent
            st.session_state.selected_role = f"{role} ({tone})"
            st.session_state.show_customizer = False
            st.success("Persona updated. Continue chatting with your new AI identity.")
            st.rerun()

# --------- 🎯 Goal Tracker Popup ---------
if st.session_state.get("show_goal_popup"):
    with st.expander("🎯 Goal Tracker", expanded=True):
        if st.button("❌ Close Goal Tracker", key="close_goal_tracker_btn"):
            st.session_state.show_goal_popup = False
            st.rerun()
        st.subheader("📌 Track your goals here!")
        st.markdown("- [ ] Example: Meditate 10 minutes daily")
        st.markdown("- [ ] Example: Finish final project")
        st.markdown("*(Goal tracker functionality coming in Day 34–35)*")


# --------- Day 30: Smart AI Insights from Memory Patterns ---------
if st.session_state.get("show_insights_popup"):
    with st.expander("🧠 AI Pattern Insights", expanded=True):
        if st.button("❌ Close", key="close_insight_popup"):
            st.session_state.show_insights_popup = False
            st.stop()

        st.markdown("Click below to analyze your memory patterns and generate insights.")
        if st.button("🧠 Analyze Patterns", key="analyze_insights"):
            with st.spinner("Analyzing your memories..."):
                insights = generate_memory_insights(st.session_state.memory_logs, client)
                st.session_state.generated_insights = insights
        if st.session_state.get("generated_insights"):
            st.markdown("### 📋 Insight Summary")
            st.markdown(st.session_state.generated_insights)

# --------- Day 36: 📈 Goal Progress Insights ---------
if st.session_state.get("show_growth_popup"):
    with st.expander("📈 Goal Progress Insights", expanded=True):
        if st.button("❌ Close", key="close_growth_popup"):
            st.session_state.show_growth_popup = False
            st.rerun()

        # STEP 2: Load data & show chart
        if "goals" not in st.session_state:
            st.session_state.goals = load_goals(username)

        goal_counts = get_memory_count_per_goal(st.session_state.memory_logs, st.session_state.goals)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.bar(goal_counts.keys(), goal_counts.values())
        ax.set_ylabel("Reflections Linked")
        ax.set_title("Goal Progress by Memory Count")
        plt.xticks(rotation=30)
        st.pyplot(fig)

        if st.button("🧠 Compare My Goals (GPT)", key="gpt_goal_compare"):
            prompt = (
                "Analyze the user's reflection progress across the following goals "
                "based on how many memories are linked to each goal. "
                "Here is the data:\n\n" +
                "\n".join([f"{goal}: {count} reflections" for goal, count in goal_counts.items()]) +
                "\n\nGive a comparative insight highlighting which goals are prioritized or neglected."
            )

            try:
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                summary = response.choices[0].message.content.strip()
                st.session_state["goal_comparison_gpt"] = summary
            except Exception as e:
                st.error(f"Failed to get GPT insight: {e}")


        if "goal_comparison_gpt" in st.session_state:
            st.markdown("**🧠 GPT Summary:**")
            st.info(st.session_state["goal_comparison_gpt"])


# --------- Day 31: Multi-Persona Comparison ---------
if st.session_state.get("show_compare_popup"):
    with st.expander("🧠 Compare Persona Reflections", expanded=True):
        if st.button("❌ Close", key="close_compare_popup"):
            st.session_state.show_compare_popup = False
            st.stop()

        memory_options = [m.get("text", "")[:60] for m in st.session_state.memory_logs]
        selected_memory = st.selectbox("Select a memory to compare", options=memory_options)

        if st.button("🔍 Compare Personas"):
            chosen_mem = next((m for m in st.session_state.memory_logs if m.get("text", "").startswith(selected_memory)), None)
            if chosen_mem:
                mem_text = chosen_mem.get("text", "")
                with st.spinner("Generating multi-perspective insights..."):
                    reflections = {}
                    for persona in ["Coach", "Mentor", "Friend", "Inner Critic"]:
                        reflections[persona] = generate_persona_reflection(mem_text, persona, client)
                st.session_state.persona_comparisons = reflections

        if st.session_state.get("persona_comparisons"):
            st.markdown("### 🧩 Multi-Perspective Reflections")
            for role, reflection in st.session_state.persona_comparisons.items():
                st.markdown(f"**{role}:** {reflection}")

# --------- Day 32: 📈 Growth & Trends ---------
if st.session_state.get("show_growth_popup"):
    with st.expander("📈 Self-Growth Trends", expanded=True):
        if st.button("❌ Close Insights Chart", key="close_growth_chart"):
            st.session_state.show_growth_popup = False
            st.stop()

        st.markdown("Visualize how your emotions and cognition evolve over time.")

        # ⏳ Prepare data by week
        from collections import defaultdict
        from datetime import datetime

        def group_by_week(memories):
            weekly_emotions = defaultdict(list)
            weekly_cognitions = defaultdict(list)
            for m in memories:
                date = datetime.strptime(m.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                week_key = date.strftime("%Y-%W")
                if m.get("emotion_tag"):
                    weekly_emotions[week_key].append(m["emotion_tag"].lower())
                if m.get("cognitive_tag"):
                    weekly_cognitions[week_key].append(m["cognitive_tag"].lower())
            return weekly_emotions, weekly_cognitions

        weekly_emotions, weekly_cognitions = group_by_week(st.session_state.memory_logs)

        # 📊 Emotion Trend Chart
        if weekly_emotions:
            st.subheader("📊 Emotion Trend")
            all_emotions = list({tag for tags in weekly_emotions.values() for tag in tags})
            emotion_counts = {week: {e: weekly_emotions[week].count(e) for e in all_emotions} for week in weekly_emotions}
            weeks = sorted(emotion_counts.keys())

            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            for e in all_emotions:
                values = [emotion_counts[w].get(e, 0) for w in weeks]
                ax.plot(weeks, values, label=e)
            ax.set_title("Emotion Frequency Over Time")
            ax.set_ylabel("Count")
            ax.set_xlabel("Week")
            ax.legend()
            plt.xticks(rotation=30)
            st.pyplot(fig)

        # 🧠 Cognition Trend Chart
        if weekly_cognitions:
            st.subheader("🧠 Cognitive Pattern Trend")
            all_cogs = list({tag for tags in weekly_cognitions.values() for tag in tags})
            cog_counts = {week: {c: weekly_cognitions[week].count(c) for c in all_cogs} for week in weekly_cognitions}
            fig2, ax2 = plt.subplots()
            for c in all_cogs:
                values = [cog_counts[w].get(c, 0) for w in weeks]
                ax2.plot(weeks, values, label=c)
            ax2.set_title("Cognitive Tags Over Time")
            ax2.set_ylabel("Count")
            ax2.set_xlabel("Week")
            ax2.legend()
            plt.xticks(rotation=30)
            st.pyplot(fig2)

        # 🧠 GPT Summary
        st.markdown("### 🧠 Monthly Growth Summary")
        if st.button("🧠 Summarize Growth"):
            with st.spinner("Analyzing growth..."):
                summary = analyze_growth_trends(st.session_state.memory_logs, client)
                st.session_state["growth_summary"] = summary

        if st.session_state.get("growth_summary"):
            st.markdown(st.session_state["growth_summary"])

# --------- Day 33: 🎯 Goal Tracker ---------
if st.session_state.get("show_goal_popup"):

    # ✅ Load goals if not already loaded
    if "goals" not in st.session_state:
        st.session_state.goals = load_goals(username)

    st.markdown("## 🎯 Personal Goals Tracker")

    # ❌ Close button
    if st.button("❌ Close", key="close_goal_popup"):
        st.session_state.show_goal_popup = False
        st.rerun()

    # ➕ Add New Goal Form
    st.markdown("### ➕ Add New Goal")
    with st.form("add_goal_form"):
        new_title = st.text_input("Goal Title")
        new_desc = st.text_area("Description")
        new_status = st.selectbox("Status", ["Active", "Completed"])
        submitted = st.form_submit_button("Add Goal")

        if submitted and new_title:
            new_goal = {
                "title": new_title,
                "description": new_desc,
                "status": new_status
            }
            st.session_state.goals.append(new_goal)
            save_goals(username, st.session_state.goals)
            st.success("Goal added!")
            st.rerun()

    # 🗂️ Display All Goals
    if st.session_state.goals:
        st.markdown("### 🗂️ Your Goals")
        for i, goal in enumerate(st.session_state.goals):
            with st.expander(f"🎯 {goal['title']} — {goal['status']}"):
                st.markdown(f"**Description:** {goal['description']}")

                # ✅ Count linked memories
                linked_memories = [
                    mem for mem in st.session_state.memory_logs
                    if goal["title"] in mem.get("linked_goals", [])
                ]
                linked_count = len(linked_memories)
                goal_target = 10  # can be dynamic later

                # ✅ Show progress bar
                st.markdown(f"**Linked Memories:** {linked_count} / {goal_target}")
                st.progress(min(linked_count / goal_target, 1.0))

                # 🧠 Day 37 – Smart Feedback Suggestions
                from datetime import datetime

                # Add created_at if missing (for legacy goals)
                if "created_at" not in goal:
                    goal["created_at"] = datetime.now().strftime("%Y-%m-%d")
                    save_goals(username, st.session_state.goals)

                # Calculate goal age in days
                created_date = datetime.strptime(goal["created_at"], "%Y-%m-%d")
                days_since_created = (datetime.now() - created_date).days

                # Feedback prompts
                feedback_msgs = []

                # ⏳ Slow progress
                if linked_count < 2 and days_since_created > 7:
                    feedback_msgs.append("You’ve linked only 1 memory in over a week — want to reflect more?")

                # ✅ Nearly complete
                if linked_count >= goal_target * 0.9 and goal["status"] != "Completed":
                    feedback_msgs.append("This goal is 90% complete — ready to mark it done or evolve it?")

                # 📚 Learning theme clustering suggestion
                if "learn" in goal["title"].lower() or "study" in goal["title"].lower():
                    feedback_msgs.append("This seems like a learning goal — want to create a 'Growth' theme?")

                # Display feedback nicely
                if feedback_msgs:
                    st.markdown("**📌 AI Suggestions:**")
                for msg in feedback_msgs:
                    st.markdown(f"""
                    <div style="background-color:#fff3cd; padding:10px; border-left:5px solid #ffc107; border-radius:6px; margin-bottom:10px;">
                    {msg}
                    </div>
                    """, unsafe_allow_html=True)


                # ✅ Show memory texts (no nested expander)
                if linked_memories:
                    st.markdown("**🧠 Linked Memories:**")
                    with st.container():
                        for mem in linked_memories:
                            st.markdown(f"- {mem['text']}")

                # 🧠 Generate Insight Button (OpenRouter)
                if st.button(f"🧠 Generate Insight", key=f"insight_btn_{i}"):
                    insight = generate_goal_insight(goal, st.session_state.memory_logs, openrouter_api_key)
                    st.session_state.goals[i]["insight"] = insight  # 🔐 Save into goal
                    save_goals(username, st.session_state.goals)    # 💾 Save to file
                    st.success("Insight saved!")
                    st.rerun()

                # 📤 Show Insight if already generated
                if "insight" in goal:
                   st.markdown("**🧠 AI Insight:**")
                   st.info(goal["insight"])
                
                   # 🗑️ Optional delete button
                   if st.button("🗑️ Delete Insight", key=f"del_insight_{i}"):
                       del st.session_state.goals[i]["insight"]
                       save_goals(username, st.session_state.goals)
                       st.rerun()



                # ✅ Update goal status
                new_status = st.selectbox("Update Status", ["Active", "Completed"],
                                          index=0 if goal["status"] == "Active" else 1,
                                          key=f"status_{i}")
                if new_status != goal["status"]:
                    st.session_state.goals[i]["status"] = new_status
                    save_goals(username, st.session_state.goals)
                    st.rerun()
=======
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

# Note: Removed st.experimental_rerun to maintain compatibility with Streamlit >= 1.35
>>>>>>> e404ebc657dd34560f6155b0ae034a0fd306a657
