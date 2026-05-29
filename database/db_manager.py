import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "interview_ai.db")

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_interviews INTEGER DEFAULT 0,
            is_verified INTEGER DEFAULT 0
        )
    """)
    
    # Email verification codes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_used INTEGER DEFAULT 0
        )
    """)
    
    # Interview sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            mode TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Conversation history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
        )
    """)
    
    conn.commit()
    conn.close()

def create_user(username, password_hash, email):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, None

def get_user(username):
    """Get user by username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_session(user_id, topic, difficulty, mode):
    """Create a new interview session"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interview_sessions (user_id, topic, difficulty, mode) VALUES (?, ?, ?, ?)",
        (user_id, topic, difficulty, mode)
    )
    conn.commit()
    session_id = cursor.lastrowid
    
    # Update user's total interviews
    cursor.execute("UPDATE users SET total_interviews = total_interviews + 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return session_id

def save_message(session_id, role, content):
    """Save a conversation message"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversation_history (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def end_session(session_id, score=0, total_questions=0):
    """End an interview session"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE interview_sessions SET ended_at = CURRENT_TIMESTAMP, score = ?, total_questions = ? WHERE id = ?",
        (score, total_questions, session_id)
    )
    conn.commit()
    conn.close()

def get_user_sessions(user_id, limit=10):
    """Get user's interview sessions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, topic, difficulty, mode, score, total_questions, started_at, ended_at
        FROM interview_sessions
        WHERE user_id = ?
        ORDER BY started_at DESC
        LIMIT ?
    """, (user_id, limit))
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_session_conversation(session_id):
    """Get conversation history for a session"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, timestamp
        FROM conversation_history
        WHERE session_id = ?
        ORDER BY timestamp ASC
    """, (session_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_user_stats(user_id):
    """Get user statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total interviews
    cursor.execute("SELECT total_interviews FROM users WHERE id = ?", (user_id,))
    total = cursor.fetchone()[0]
    
    # Average score
    cursor.execute("""
        SELECT AVG(CAST(score AS FLOAT) / NULLIF(total_questions, 0) * 100) as avg_score
        FROM interview_sessions
        WHERE user_id = ? AND total_questions > 0
    """, (user_id,))
    avg_score = cursor.fetchone()[0] or 0
    
    # Topics practiced
    cursor.execute("""
        SELECT topic, COUNT(*) as count
        FROM interview_sessions
        WHERE user_id = ?
        GROUP BY topic
        ORDER BY count DESC
    """, (user_id,))
    topics = cursor.fetchall()
    
    conn.close()
    return {
        "total_interviews": total,
        "avg_score": round(avg_score, 1),
        "topics": topics
    }

def store_verification_code(email, code, expires_at):
    """Store verification code for email"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO verification_codes (email, code, expires_at) VALUES (?, ?, ?)",
        (email, code, expires_at)
    )
    conn.commit()
    conn.close()

def verify_code(email, code):
    """Verify the code for an email"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM verification_codes
        WHERE email = ? AND code = ? AND is_used = 0 AND expires_at > CURRENT_TIMESTAMP
    """, (email, code))
    result = cursor.fetchone()
    
    if result:
        # Mark code as used
        cursor.execute("UPDATE verification_codes SET is_used = 1 WHERE id = ?", (result[0],))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def check_email_exists(email):
    """Check if email already exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Initialize database on import
init_database()
