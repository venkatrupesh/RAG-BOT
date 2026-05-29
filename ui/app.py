# ui/app.py

import streamlit as st
import sys
import os
import hashlib
import json
from datetime import datetime
sys.path.append(".")

from groq import Groq
from dotenv import load_dotenv
from retrieval.retriever import retrieve_context

# Try to import voice interview (optional)
try:
    from ui.voice_interview import show_voice_interview
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Voice libraries not installed. Voice mode will be disabled.")

load_dotenv()

st.set_page_config(
    page_title="InterviewAI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
    /* ── Reset & Base ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    html, body, .stApp {
        background-color: #f9fafb;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #111827;
    }

    /* ── Login Page ── */
    .auth-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
    }

    .auth-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }

    .auth-logo {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        text-align: center;
        margin-bottom: 0.25rem;
    }

    .auth-sub {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1.75rem;
    }

    /* ── Tabs ── */
    [data-testid="stTabs"] button {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6b7280;
        border: none;
        background: none;
        padding: 0.5rem 1rem;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #111827;
        border-bottom: 2px solid #111827;
        background: none;
    }

    [data-testid="stTabs"] [data-testid="stTabsBar"] {
        border-bottom: 1px solid #e5e7eb;
        gap: 0;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.85rem !important;
        font-size: 0.9rem !important;
        background: #ffffff !important;
        color: #111827 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6b7280 !important;
    }

    .stTextInput label {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        margin-bottom: 0.25rem !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.55rem 1.2rem;
        border: 1px solid #d1d5db;
        background: #ffffff;
        color: #374151;
        transition: background 0.15s, border-color 0.15s;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        background: #f3f4f6;
        border-color: #9ca3af;
    }

    .stButton > button:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Primary button (full-width auth buttons) */
    div[data-testid="column"] .stButton > button,
    .auth-card .stButton > button {
        background: #111827;
        color: #ffffff;
        border: none;
        width: 100%;
    }

    div[data-testid="column"] .stButton > button:hover,
    .auth-card .stButton > button:hover {
        background: #1f2937;
    }

    /* MCQ option buttons */
    .mcq-container .stButton > button {
        background: #ffffff;
        border: 2px solid #e5e7eb;
        color: #374151;
        text-align: left;
        padding: 0.85rem 1rem;
        font-size: 0.92rem;
        border-radius: 10px;
        transition: all 0.2s;
    }

    .mcq-container .stButton > button:hover {
        border-color: #111827;
        background: #f9fafb;
        transform: translateX(2px);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.82rem;
        font-weight: 500;
        color: #374151;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div:focus {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff;
        color: #374151;
        border: 1px solid #e5e7eb;
        font-size: 0.85rem;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #f9fafb;
        border-color: #d1d5db;
    }

    /* ── Chat ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 0.92rem;
        line-height: 1.65;
        color: #111827;
    }

    [data-testid="stChatInput"] textarea {
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        font-size: 0.9rem !important;
        background: #ffffff !important;
        box-shadow: none !important;
        padding: 0.75rem 1rem !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #6b7280 !important;
        box-shadow: none !important;
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1rem 0;
    }

    /* ── Info / Alert boxes ── */
    .stAlert {
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        border: none !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: #111827 !important;
        border-radius: 4px;
    }

    .stProgress > div {
        background: #e5e7eb !important;
        border-radius: 4px;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #111827 !important;
    }

    /* ── Radio ── */
    .stRadio > div {
        gap: 0.4rem;
    }

    .stRadio > div label {
        font-size: 0.88rem !important;
        color: #374151 !important;
    }

    /* ── MCQ Container ── */
    .mcq-container {
        margin: 1.5rem 0;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    .mcq-question {
        font-size: 1.05rem;
        font-weight: 500;
        color: #111827;
        margin-bottom: 1.25rem;
        line-height: 1.6;
    }

    /* Remove red/blue focus rings everywhere */
    * { outline: none !important; }
    *:focus { box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──
USERS_FILE = "users.json"
TOPICS_WITH_RESOURCES = ["python", "java", "sql"]

TOPICS = {
    "Python": "🐍",
    "Java": "☕",
    "JavaScript": "⚡",
    "C++": "⚙️",
    "SQL": "🗄️",
    "Data Science": "📊",
    "Machine Learning": "🤖",
    "System Design": "🏗️",
}

DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]
SKIP_COMMANDS = ["pass", "skip", "next", "idk"]

RAG_PROMPT = """You are a professional technical interviewer conducting a {topic} interview.
You have verified reference material below. Use it to ask questions AND verify answers.

RULES:
- Ask questions strictly based on the context
- After the candidate answers, compare with context and give: ✅ Correct / ⚠️ Partial / ❌ Incorrect
- If wrong, show the correct answer from context
- If candidate says pass/skip → reveal correct answer from context, move on
- One question at a time
- After 5 questions give score out of 10

Difficulty: {difficulty}
Reference Material:
{context}"""

LLM_PROMPT = """You are a professional technical interviewer conducting a {topic} interview.
Use your own trained knowledge to ask and evaluate questions.

RULES:
- Ask relevant {topic} questions based on your knowledge
- Give feedback: ✅ Correct / ⚠️ Partial / ❌ Incorrect
- If wrong, explain the correct answer
- If candidate says pass/skip → give correct answer, move on
- One question at a time
- After 5 questions give score out of 10

Difficulty: {difficulty}"""

MCQ_PROMPT = """You are a professional technical interviewer conducting a {topic} MCQ test.

RULES:
- Generate ONE multiple choice question at a time
- Format EXACTLY as:
  Question: [Your question here]
  A) [Option A]
  B) [Option B]
  C) [Option C]
  D) [Option D]
  
- After user answers (A, B, C, or D), respond with:
  ✅ Correct! The answer is [X]. [Brief explanation]
  OR
  ❌ Incorrect. The correct answer is [X]. [Brief explanation]
  
  Then immediately provide the next question in the same format.
  
- Keep questions relevant to {topic} at {difficulty} level
- After 10 questions, show final score: "🎉 Test Complete! Final Score: X/10"
- Make options clear and distinct
- Only one correct answer per question

Difficulty: {difficulty}"""

VOICE_PROMPT = """You are a professional technical interviewer conducting a {topic} voice interview.

RULES:
- Ask clear, concise questions suitable for voice responses
- Keep questions conversational and natural
- After the candidate answers, provide brief feedback: ✅ Good / ⚠️ Needs improvement / ❌ Incorrect
- If wrong, give a short correct answer
- If candidate says pass/skip → give correct answer briefly, move on
- One question at a time
- After 5 questions give score out of 10
- Keep responses short and clear for voice interaction

Difficulty: {difficulty}"""

# ── User Management ──
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username: str, password: str, email: str) -> tuple[bool, str]:
    users = load_users()
    if username in users:
        return False, "Username already exists."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "interviews": 0
    }
    save_users(users)
    return True, "Account created! You can now sign in."

def login_user(username: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "Username not found."
    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password."
    return True, "Login successful!"

# ── Interview Logic ──
def has_resources(topic: str) -> bool:
    return topic.lower() in TOPICS_WITH_RESOURCES

def get_system_prompt(user_input: str, topic: str, difficulty: str, mode: str = "Text") -> tuple[str, str]:
    if mode == "Voice":
        return VOICE_PROMPT.format(topic=topic, difficulty=difficulty), "Voice"
    elif mode == "MCQ":
        return MCQ_PROMPT.format(topic=topic, difficulty=difficulty), "MCQ"
    elif has_resources(topic):
        query = f"{topic} interview question answer" if user_input.lower().strip() in SKIP_COMMANDS else f"{topic} {user_input}"
        context = retrieve_context(query, k=5)
        return RAG_PROMPT.format(topic=topic, difficulty=difficulty, context=context), "RAG"
    else:
        return LLM_PROMPT.format(topic=topic, difficulty=difficulty), "LLM"

def ask_groq(system: str, history: list) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "system", "content": system}] + history
    )
    return response.choices[0].message.content

# ── Session State ──
def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "history": [],
        "topic": "Python",
        "difficulty": "Intermediate",
        "interview_mode": "Text",
        "interview_started": False,
        "question_count": 0,
        "score": 0,
        "total_questions": 0,
        "pending_answer": None,
        "sidebar_visible": True,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()


# ══════════════════════════════════════════════════════════════════════════
# LOGIN / SIGNUP PAGE
# ══════════════════════════════════════════════════════════════════════════
def show_login():
    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

        # Logo / Brand
        st.markdown(
            "<div style='text-align:center; font-size:1.7rem; font-weight:700; color:#111827; margin-bottom:4px;'>💬 InterviewAI</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='text-align:center; color:#6b7280; font-size:0.9rem; margin-bottom:2rem;'>Your AI-powered interview practice platform</div>",
            unsafe_allow_html=True
        )

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.button("Sign In", key="login_btn", use_container_width=True):
                if username and password:
                    ok, msg = login_user(username, password)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")

        with tab_signup:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            
            # Simple registration without email verification
            new_user  = st.text_input("Username", placeholder="Choose a username", key="reg_user")
            new_email = st.text_input("Email", placeholder="your@email.com", key="reg_email")
            new_pass  = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="reg_pass")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.button("Create Account", key="reg_btn", use_container_width=True):
                if new_user and new_email and new_pass:
                    ok, msg = register_user(new_user, new_pass, new_email)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("⚠️ Please fill in all fields.")


# ══════════════════════════════════════════════════════════════════════════
# MAIN CHAT INTERFACE
# ══════════════════════════════════════════════════════════════════════════
def show_chat():
    # ── Sidebar Toggle ──
    toggle_col1, toggle_col2 = st.columns([0.05, 0.95])
    with toggle_col1:
        if st.button("☰", key="sidebar_toggle"):
            st.session_state.sidebar_visible = not st.session_state.sidebar_visible

    # Inject CSS to hide/show sidebar
    if not st.session_state.sidebar_visible:
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            .main .block-container {
                padding-left: 1rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    topic      = st.session_state.topic
    difficulty = st.session_state.difficulty

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(
            f"<div style='font-size:1rem; font-weight:600; color:#111827; margin-bottom:0.1rem;'>💬 InterviewAI</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:0.82rem; color:#6b7280; margin-bottom:1rem;'>Signed in as <b>{st.session_state.username}</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("---")

        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#374151; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:0.05em;'>Mode</div>", unsafe_allow_html=True)
        
        # Show voice mode only if libraries are installed
        if VOICE_AVAILABLE:
            mode_options = ["Text Interview", "Voice Interview", "MCQ Test"]
            mode_index = 0 if st.session_state.interview_mode == "Text" else (1 if st.session_state.interview_mode == "Voice" else 2)
        else:
            mode_options = ["Text Interview", "MCQ Test"]
            mode_index = 0 if st.session_state.interview_mode == "Text" else 1
            if st.session_state.interview_mode == "Voice":
                st.session_state.interview_mode = "Text"  # Fallback to text
        
        interview_mode = st.radio(
            "Mode",
            mode_options,
            index=mode_index,
            label_visibility="collapsed"
        )
        
        if interview_mode == "Text Interview":
            st.session_state.interview_mode = "Text"
        elif interview_mode == "Voice Interview":
            st.session_state.interview_mode = "Voice"
        else:
            st.session_state.interview_mode = "MCQ"
        
        # Show installation hint if voice not available
        if not VOICE_AVAILABLE and interview_mode == "Text Interview":
            st.info("💡 **Voice mode disabled**. Install voice libraries to enable:\n```\npip install gTTS SpeechRecognition pyaudio audio-recorder-streamlit\n```")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#374151; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:0.05em;'>Topic</div>", unsafe_allow_html=True)
        topic_list = list(TOPICS.keys())
        topic = st.selectbox("Topic", topic_list, index=topic_list.index(st.session_state.topic), label_visibility="collapsed")
        st.session_state.topic = topic

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#374151; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:0.05em;'>Difficulty</div>", unsafe_allow_html=True)
        difficulty = st.selectbox("Difficulty", DIFFICULTIES, index=DIFFICULTIES.index(st.session_state.difficulty), label_visibility="collapsed")
        st.session_state.difficulty = difficulty

        if st.session_state.interview_mode == "Text":
            mode_tag = "RAG Mode" if has_resources(topic) else "LLM Mode"
            st.markdown(
                f"<div style='font-size:0.78rem; color:#6b7280; margin-top:0.5rem;'>Source: {mode_tag}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Stats
        st.markdown(
            f"<div style='font-size:0.82rem; color:#374151;'>Questions answered: <b>{st.session_state.question_count}</b></div>",
            unsafe_allow_html=True
        )
        if st.session_state.interview_mode == "MCQ" and st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.markdown(
                f"<div style='font-size:0.82rem; color:#374151; margin-top:0.3rem;'>Score: <b>{st.session_state.score}/{st.session_state.total_questions}</b> &nbsp;·&nbsp; {accuracy:.0f}%</div>",
                unsafe_allow_html=True
            )
            st.progress(accuracy / 100)

        st.markdown("---")

        if st.button("New Interview", use_container_width=True):
            st.session_state.history = []
            st.session_state.interview_started = False
            st.session_state.question_count = 0
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.pending_answer = None
            st.rerun()

        if st.button("Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ── Header ──
    mode_label = "MCQ Test" if st.session_state.interview_mode == "MCQ" else ("Voice Interview" if st.session_state.interview_mode == "Voice" else "Text Interview")
    st.markdown(
        f"<div style='font-size:0.85rem; color:#6b7280; padding:0.5rem 0 0.25rem 0;'>"
        f"{TOPICS.get(topic, '')} <b style='color:#111827'>{topic}</b> &nbsp;·&nbsp; {difficulty} &nbsp;·&nbsp; {mode_label}"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("<hr style='margin:0 0 1rem 0;'>", unsafe_allow_html=True)
    
    # ── Voice Interview Mode ──
    if st.session_state.interview_mode == "Voice":
        if VOICE_AVAILABLE:
            show_voice_interview(st.session_state.username, topic, difficulty, get_system_prompt, ask_groq)
            return
        else:
            st.error("❌ Voice mode is not available. Please install voice libraries:")
            st.code("pip install gTTS SpeechRecognition pyaudio audio-recorder-streamlit")
            st.info("Or run: install_voice.bat")
            if st.button("Switch to Text Mode"):
                st.session_state.interview_mode = "Text"
                st.rerun()
            return

    # ── Start Interview ──
    if not st.session_state.interview_started:
        # Pre-generate first question immediately without spinner
        if st.session_state.interview_mode == "MCQ":
            start_msg = f"Start a {difficulty} level {topic} MCQ test. Generate the first multiple choice question."
        elif st.session_state.interview_mode == "Voice":
            start_msg = f"Start a {difficulty} level {topic} voice interview. Greet the candidate briefly and ask the first question in a conversational way."
        else:
            start_msg = f"Start a {difficulty} level {topic} interview. Greet the candidate and ask the first question."
        system, _ = get_system_prompt(start_msg, topic, difficulty, st.session_state.interview_mode)
        response = ask_groq(system, [{"role": "user", "content": start_msg}])
        st.session_state.history = [{"role": "assistant", "content": response}]
        st.session_state.interview_started = True
        st.session_state.question_count = 1

    # ── Chat History ──
    for msg in st.session_state.history:
        role = msg["role"]
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # ── MCQ Options Display ──
    if st.session_state.interview_mode == "MCQ" and st.session_state.history:
        last_msg = st.session_state.history[-1]
        if last_msg["role"] == "assistant":
            content = last_msg["content"]
            # Check if this is a question (contains options A, B, C, D)
            if "A)" in content and "B)" in content and "C)" in content and "D)" in content:
                # Extract question and options
                lines = content.split("\n")
                question = ""
                options = {"A": "", "B": "", "C": "", "D": ""}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("Question:"):
                        question = line.replace("Question:", "").strip()
                    elif line.startswith("A)"):
                        options["A"] = line[2:].strip()
                    elif line.startswith("B)"):
                        options["B"] = line[2:].strip()
                    elif line.startswith("C)"):
                        options["C"] = line[2:].strip()
                    elif line.startswith("D)"):
                        options["D"] = line[2:].strip()
                
                if question and any(options.values()):
                    st.markdown("<div class='mcq-container'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='mcq-question'>{question}</div>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🅰️ {options['A']}", key="opt_a", use_container_width=True):
                            st.session_state.pending_answer = "A"
                            st.rerun()
                        if st.button(f"🅲 {options['C']}", key="opt_c", use_container_width=True):
                            st.session_state.pending_answer = "C"
                            st.rerun()
                    with col2:
                        if st.button(f"🅱️ {options['B']}", key="opt_b", use_container_width=True):
                            st.session_state.pending_answer = "B"
                            st.rerun()
                        if st.button(f"🅳 {options['D']}", key="opt_d", use_container_width=True):
                            st.session_state.pending_answer = "D"
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)

    # ── Input ──
    # Handle pending MCQ answer from button click
    if st.session_state.get("pending_answer"):
        user_input = st.session_state.pending_answer
        st.session_state.pending_answer = None
        
        st.session_state.history.append({"role": "user", "content": user_input})
        
        with st.spinner("Checking answer..."):
            system, _ = get_system_prompt(user_input, topic, difficulty, st.session_state.interview_mode)
            response = ask_groq(system, st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})
            st.session_state.question_count += 1
            
            if st.session_state.interview_mode == "MCQ":
                st.session_state.total_questions += 1
                if "✅ Correct" in response or "Correct!" in response:
                    st.session_state.score += 1
        
        st.rerun()
    
    placeholder = "Type A, B, C or D..." if st.session_state.interview_mode == "MCQ" else ("Speak your answer or type it here..." if st.session_state.interview_mode == "Voice" else "Type your answer here...")
    user_input = st.chat_input(placeholder)

    if user_input:
        if user_input.lower() in ["quit", "exit", "bye"]:
            if st.session_state.interview_mode == "MCQ" and st.session_state.total_questions > 0:
                st.success(f"Test ended. Final Score: {st.session_state.score}/{st.session_state.total_questions}")
            else:
                st.success("Interview ended. Click 'New Interview' to start again.")
            return

        st.session_state.history.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            system, _ = get_system_prompt(user_input, topic, difficulty, st.session_state.interview_mode)
            response = ask_groq(system, st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})
            st.session_state.question_count += 1

            if st.session_state.interview_mode == "MCQ":
                st.session_state.total_questions += 1
                if "✅ Correct" in response or "Correct!" in response:
                    st.session_state.score += 1

        st.rerun()


# ── Router ──
if not st.session_state.logged_in:
    show_login()
else:
    show_chat()
