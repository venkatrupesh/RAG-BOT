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

# Optional imports - handle gracefully if not available
try:
    from retrieval.retriever import retrieve_context
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("RAG libraries not installed. RAG mode will be disabled.")
    def retrieve_context(query, k=5):
        return "No context available"

try:
    from database.db_manager import (
        get_user, create_session, save_message, end_session, 
        get_user_sessions, get_session_conversation
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("Database not available. Using in-memory storage.")
    # Simple fallback functions
    def get_user(username):
        users = load_users()
        if username in users:
            user_data = users[username]
            return (username, username, user_data["password"], user_data.get("email", ""))
        return None
    def create_session(user_id, topic, difficulty, mode):
        return f"session_{datetime.now().timestamp()}"
    def save_message(session_id, role, content):
        return True
    def end_session(session_id, score, total):
        return True
    def get_user_sessions(user_id, limit=100):
        return []
    def get_session_conversation(session_id):
        return []

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
    initial_sidebar_state="expanded"
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
        background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
        border-right: 1px solid #e5e7eb;
        padding: 1.5rem 1rem;
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
        border-radius: 10px !important;
        font-size: 0.88rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
        background: #ffffff !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #9ca3af !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08) !important;
    }

    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio > div {
        background: #ffffff;
        border-radius: 10px;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    
    [data-testid="stSidebar"] .stRadio > div label {
        padding: 0.6rem 0.8rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > div label:hover {
        background: #f3f4f6 !important;
    }

    /* Sidebar Buttons - Professional Clean Style */
    [data-testid="stSidebar"] .stButton > button {
        background: #ffffff;
        color: #374151;
        border: 1.5px solid #e5e7eb;
        font-size: 0.88rem;
        font-weight: 600;
        padding: 0.75rem 1.2rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.25s ease;
        letter-spacing: 0.01em;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #f9fafb;
        border-color: #d1d5db;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }
    
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* New Interview Button - Blue Accent */
    [data-testid="stSidebar"] button[key="new_interview_btn"] {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.25) !important;
    }
    
    [data-testid="stSidebar"] button[key="new_interview_btn"]:hover {
        background: #2563eb !important;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.35) !important;
    }

    /* History Button - Neutral with Icon */
    [data-testid="stSidebar"] button[key="history_btn"] {
        background: #ffffff !important;
        color: #374151 !important;
        border: 1.5px solid #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] button[key="history_btn"]:hover {
        background: #f3f4f6 !important;
        border-color: #d1d5db !important;
    }

    /* Sign Out Button - Clean Red Accent */
    [data-testid="stSidebar"] button[key="signout_btn"] {
        background: #ffffff !important;
        color: #dc2626 !important;
        border: 1.5px solid #fecaca !important;
    }
    
    [data-testid="stSidebar"] button[key="signout_btn"]:hover {
        background: #fef2f2 !important;
        border-color: #fca5a5 !important;
        color: #b91c1c !important;
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
    user = get_user(username)
    if not user:
        return False, "Username not found."
    if user[2] != hash_password(password):
        return False, "Incorrect password."
    st.session_state.user_id = user[0]
    return True, "Login successful!"

# ── Interview Logic ──
def has_resources(topic: str) -> bool:
    if not RAG_AVAILABLE:
        return False
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
        "user_id": None,
        "current_session_id": None,
        "history": [],
        "topic": "Python",
        "difficulty": "Intermediate",
        "interview_mode": "Text",
        "interview_started": False,
        "question_count": 0,
        "score": 0,
        "total_questions": 0,
        "pending_answer": None,
        "show_history": False,
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
    topic      = st.session_state.topic
    difficulty = st.session_state.difficulty

    # ── Sidebar ──
    difficulty_icons = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}
    
    with st.sidebar:
        st.markdown(
            f"<div style='font-size:1.1rem; font-weight:700; color:#111827; margin-bottom:0.2rem;'>💬 InterviewAI</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:0.82rem; color:#6b7280; margin-bottom:1.2rem;'>👤 <b>{st.session_state.username}</b></div>",
            unsafe_allow_html=True
        )
        st.markdown("<hr style='margin:0.5rem 0 1rem 0; border:none; border-top:1px solid #e5e7eb;'>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#6b7280; margin-bottom:0.6rem; text-transform:uppercase; letter-spacing:0.08em;'>🎯 Interview Mode</div>", unsafe_allow_html=True)
        
        if VOICE_AVAILABLE:
            mode_options = ["💬 Text Interview", "🎤 Voice Interview", "📝 MCQ Test", "📊 Analytics Dashboard"]
            mode_index = 0 if st.session_state.interview_mode == "Text" else (1 if st.session_state.interview_mode == "Voice" else (2 if st.session_state.interview_mode == "MCQ" else 3))
        else:
            mode_options = ["💬 Text Interview", "📝 MCQ Test", "📊 Analytics Dashboard"]
            mode_index = 0 if st.session_state.interview_mode == "Text" else (1 if st.session_state.interview_mode == "MCQ" else 2)
            if st.session_state.interview_mode == "Voice":
                st.session_state.interview_mode = "Text"
        
        interview_mode = st.radio(
            "Mode",
            mode_options,
            index=mode_index,
            label_visibility="collapsed"
        )
        
        if "Text" in interview_mode:
            st.session_state.interview_mode = "Text"
        elif "Voice" in interview_mode:
            st.session_state.interview_mode = "Voice"
        elif "Analytics" in interview_mode:
            st.session_state.interview_mode = "Analytics"
        else:
            st.session_state.interview_mode = "MCQ"

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#6b7280; margin-bottom:0.6rem; text-transform:uppercase; letter-spacing:0.08em;'>📚 Topic</div>", unsafe_allow_html=True)
        topic_options = [f"{TOPICS[t]} {t}" for t in TOPICS.keys()]
        current_topic_display = f"{TOPICS[st.session_state.topic]} {st.session_state.topic}"
        selected_topic = st.selectbox(
            "Topic", 
            topic_options, 
            index=topic_options.index(current_topic_display),
            label_visibility="collapsed"
        )
        for t in TOPICS.keys():
            if t in selected_topic:
                st.session_state.topic = t
                topic = t
                break

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#6b7280; margin-bottom:0.6rem; text-transform:uppercase; letter-spacing:0.08em;'>⚡ Difficulty</div>", unsafe_allow_html=True)
        difficulty_options = [f"{difficulty_icons[d]} {d}" for d in DIFFICULTIES]
        current_diff_display = f"{difficulty_icons[st.session_state.difficulty]} {st.session_state.difficulty}"
        selected_difficulty = st.selectbox(
            "Difficulty", 
            difficulty_options, 
            index=difficulty_options.index(current_diff_display),
            label_visibility="collapsed"
        )
        for d in DIFFICULTIES:
            if d in selected_difficulty:
                st.session_state.difficulty = d
                difficulty = d
                break

        if st.session_state.interview_mode == "Text":
            mode_tag = "🔍 RAG Mode" if has_resources(topic) else "🧠 LLM Mode"
            st.markdown(
                f"<div style='font-size:0.78rem; color:#6b7280; margin-top:0.6rem; padding:0.4rem 0.6rem; background:#f9fafb; border-radius:6px; text-align:center;'>{mode_tag}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<hr style='margin:1rem 0; border:none; border-top:1px solid #e5e7eb;'>", unsafe_allow_html=True)

        st.markdown(
            f"<div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:1rem; border-radius:10px; margin-bottom:1rem;'>" 
            f"<div style='color:#ffffff; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.3rem;'>📊 Progress</div>"
            f"<div style='color:#ffffff; font-size:1.4rem; font-weight:700;'>{st.session_state.question_count}</div>"
            f"<div style='color:rgba(255,255,255,0.8); font-size:0.8rem;'>Questions Answered</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        
        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.markdown(
                f"<div style='background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding:1rem; border-radius:10px; margin-bottom:1rem;'>" 
                f"<div style='color:#ffffff; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.3rem;'>🎯 Score</div>"
                f"<div style='color:#ffffff; font-size:1.4rem; font-weight:700;'>{int(st.session_state.score)}/{st.session_state.total_questions}</div>"
                f"<div style='color:rgba(255,255,255,0.8); font-size:0.8rem;'>Accuracy: {accuracy:.0f}%</div>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.progress(accuracy / 100)

        st.markdown("<hr style='margin:1rem 0; border:none; border-top:1px solid #e5e7eb;'>", unsafe_allow_html=True)

        if st.button("🔄 New Interview", use_container_width=True, key="new_interview_btn"):
            # End current session
            if st.session_state.current_session_id:
                end_session(
                    st.session_state.current_session_id,
                    st.session_state.score,
                    st.session_state.total_questions
                )
            # Reset all interview state including voice
            st.session_state.history = []
            st.session_state.interview_started = False
            st.session_state.question_count = 0
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.pending_answer = None
            st.session_state.current_session_id = None
            # Reset voice-specific state
            if 'voice_history' in st.session_state:
                st.session_state.voice_history = []
            if 'voice_started' in st.session_state:
                st.session_state.voice_started = False
            if 'voice_question_count' in st.session_state:
                st.session_state.voice_question_count = 0
            st.rerun()

        if st.button("📋 History", use_container_width=True, key="history_btn"):
            st.session_state.show_history = not st.session_state.show_history
            st.rerun()

        if st.button("→ Sign Out", use_container_width=True, key="signout_btn"):
            # End current session before logout
            if st.session_state.current_session_id:
                end_session(
                    st.session_state.current_session_id,
                    st.session_state.score,
                    st.session_state.total_questions
                )
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ── Header ──
    mode_label = "📝 MCQ Test" if st.session_state.interview_mode == "MCQ" else ("🎤 Voice Interview" if st.session_state.interview_mode == "Voice" else ("📊 Analytics Dashboard" if st.session_state.interview_mode == "Analytics" else "💬 Text Interview"))
    st.markdown(
        f"<div style='font-size:0.9rem; color:#6b7280; padding:0.5rem 0 0.25rem 0;'>"
        f"{TOPICS.get(topic, '')} <b style='color:#111827'>{topic}</b> &nbsp;·&nbsp; "
        f"{difficulty_icons.get(difficulty, '')} <b style='color:#111827'>{difficulty}</b> &nbsp;·&nbsp; {mode_label}"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("<hr style='margin:0 0 1rem 0;'>", unsafe_allow_html=True)
    
    # ── Analytics Dashboard Mode ──
    if st.session_state.interview_mode == "Analytics":
        try:
            from ui.analytics_dashboard import render_analytics_dashboard
            render_analytics_dashboard(st.session_state.user_id, get_user_sessions, ask_groq)
            return
        except Exception as e:
            st.error(f"❌ Error loading analytics: {str(e)}")
            st.info("💡 Try switching to another mode")
            if st.button("Switch to Text Mode"):
                st.session_state.interview_mode = "Text"
                st.rerun()
            return
    
    # ── Voice Interview Mode ──
    if st.session_state.interview_mode == "Voice":
        if VOICE_AVAILABLE:
            # Create session if not exists (before showing voice interview)
            if not st.session_state.current_session_id:
                st.session_state.current_session_id = create_session(
                    st.session_state.user_id, topic, difficulty, st.session_state.interview_mode
                )
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
    
    # ── Show History ──
    if st.session_state.show_history:
        st.markdown("### 📜 Interview History")
        st.markdown("---")
        
        sessions = get_user_sessions(st.session_state.user_id)
        
        if not sessions:
            st.info("No interview history yet. Start your first interview!")
        else:
            for session in sessions:
                # Unpack: id, topic, difficulty, mode, score, total_questions, started_at, ended_at
                session_id, topic_name, difficulty_level, mode, score, total, start_time, end_time = session
                
                # Format time - show exact timestamp from database
                try:
                    # SQLite returns timestamps as strings in format: YYYY-MM-DD HH:MM:SS
                    if start_time:
                        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        formatted_time = start_dt.strftime("%b %d, %Y • %I:%M %p")
                    else:
                        formatted_time = "Unknown time"
                except Exception as e:
                    # Fallback: show raw timestamp
                    formatted_time = str(start_time) if start_time else "Unknown time"
                
                # Calculate duration if ended
                duration = ""
                if end_time and start_time:
                    try:
                        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        duration_mins = int((end_dt - start_dt).total_seconds() / 60)
                        if duration_mins > 0:
                            duration = f" • {duration_mins} min"
                        elif duration_mins == 0:
                            duration_secs = int((end_dt - start_dt).total_seconds())
                            if duration_secs > 0:
                                duration = f" • {duration_secs} sec"
                    except Exception:
                        pass
                
                # Score display
                score_display = ""
                if score is not None and total is not None and total > 0:
                    accuracy = (score / total) * 100
                    score_display = f" • Score: {score}/{total} ({accuracy:.0f}%)"
                
                # Create expandable session card
                with st.expander(f"🎯 {topic_name} - {difficulty_level} ({mode}) - {formatted_time}"):
                    st.markdown(f"**Started:** {formatted_time}{duration}{score_display}")
                    
                    # Get conversation
                    conversation = get_session_conversation(session_id)
                    
                    if conversation:
                        st.markdown("**Conversation:**")
                        for role, content, timestamp in conversation:
                            avatar = "🤖" if role == "assistant" else "👤"
                            with st.chat_message(role, avatar=avatar):
                                st.markdown(content)
                    else:
                        st.info("No conversation recorded for this session.")
                    
                    # Option to load this session
                    if st.button("📥 Load This Session", key=f"load_{session_id}"):
                        st.session_state.show_history = False
                        st.session_state.current_session_id = session_id
                        st.session_state.topic = topic_name
                        st.session_state.difficulty = difficulty_level
                        st.session_state.interview_mode = mode
                        st.session_state.interview_started = True
                        
                        # Load conversation into history
                        st.session_state.history = []
                        for role, content, timestamp in conversation:
                            st.session_state.history.append({"role": role, "content": content})
                        
                        st.session_state.question_count = len([m for m in conversation if m[0] == "assistant"])
                        if score is not None:
                            st.session_state.score = score
                        if total is not None:
                            st.session_state.total_questions = total
                        
                        st.rerun()
        
        st.markdown("---")
        if st.button("← Back to Interview"):
            st.session_state.show_history = False
            st.rerun()
        
        return

    # ── Start Interview ──
    if not st.session_state.interview_started:
        # Create new session in database
        if not st.session_state.current_session_id:
            st.session_state.current_session_id = create_session(
                st.session_state.user_id, topic, difficulty, st.session_state.interview_mode
            )
            print(f"DEBUG: Created new session ID: {st.session_state.current_session_id}")
        
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
        
        # Save to database
        print(f"DEBUG: Saving first message to session {st.session_state.current_session_id}")
        result = save_message(st.session_state.current_session_id, "assistant", response)
        print(f"DEBUG: Save result: {result}")

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
        print(f"DEBUG: Saving user message to session {st.session_state.current_session_id}")
        save_message(st.session_state.current_session_id, "user", user_input)
        
        with st.spinner("Checking answer..."):
            system, _ = get_system_prompt(user_input, topic, difficulty, st.session_state.interview_mode)
            response = ask_groq(system, st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})
            print(f"DEBUG: Saving assistant message to session {st.session_state.current_session_id}")
            save_message(st.session_state.current_session_id, "assistant", response)
            st.session_state.question_count += 1
            
            if st.session_state.interview_mode == "MCQ":
                st.session_state.total_questions += 1
                if "✅ Correct" in response or "Correct!" in response:
                    st.session_state.score += 1
            else:
                # Track score for Text/Voice interviews
                st.session_state.total_questions += 1
                if "✅" in response or "Correct" in response.split("\n")[0]:
                    st.session_state.score += 1
                elif "⚠️" in response or "Partial" in response:
                    st.session_state.score += 0.5
            
            # Update session continuously
            end_session(
                st.session_state.current_session_id,
                int(st.session_state.score),
                st.session_state.total_questions
            )
        
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
        save_message(st.session_state.current_session_id, "user", user_input)

        with st.spinner("Thinking..."):
            system, _ = get_system_prompt(user_input, topic, difficulty, st.session_state.interview_mode)
            response = ask_groq(system, st.session_state.history)
            st.session_state.history.append({"role": "assistant", "content": response})
            save_message(st.session_state.current_session_id, "assistant", response)
            st.session_state.question_count += 1

            if st.session_state.interview_mode == "MCQ":
                st.session_state.total_questions += 1
                if "✅ Correct" in response or "Correct!" in response:
                    st.session_state.score += 1
            else:
                # Track score for Text/Voice interviews based on feedback
                st.session_state.total_questions += 1
                if "✅" in response or "Correct" in response.split("\n")[0]:
                    st.session_state.score += 1
                elif "⚠️" in response or "Partial" in response:
                    st.session_state.score += 0.5
            
            # Update session continuously
            end_session(
                st.session_state.current_session_id,
                int(st.session_state.score),
                st.session_state.total_questions
            )

        st.rerun()


# ── Router ──
if not st.session_state.logged_in:
    show_login()
else:
    show_chat()
