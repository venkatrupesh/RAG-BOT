import streamlit as st
from database import db_manager as db
from datetime import datetime

def show_history_page(user_id):
    """Display user's interview history"""
    
    st.markdown("""
    <div style="padding:20px 32px;">
        <h2 style="font-family:'Plus Jakarta Sans',sans-serif;color:#18181b;margin-bottom:24px;">
            📚 Interview History
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user stats
    stats = db.get_user_stats(user_id)
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#f8f9fb;border:1px solid #ebebeb;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:700;color:#4a7fa5;">{stats['total_interviews']}</div>
            <div style="font-size:0.85rem;color:#71717a;margin-top:8px;">Total Interviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:#f8f9fb;border:1px solid #ebebeb;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:700;color:#16a34a;">{stats['avg_score']}%</div>
            <div style="font-size:0.85rem;color:#71717a;margin-top:8px;">Average Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_topic = stats['topics'][0][0] if stats['topics'] else "None"
        st.markdown(f"""
        <div style="background:#f8f9fb;border:1px solid #ebebeb;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:1.5rem;font-weight:700;color:#d97706;">{top_topic}</div>
            <div style="font-size:0.85rem;color:#71717a;margin-top:8px;">Top Topic</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # Get sessions
    sessions = db.get_user_sessions(user_id, limit=20)
    
    if not sessions:
        st.info("No interview history yet. Start your first interview!")
        return
    
    # Display sessions
    for session in sessions:
        session_id, topic, difficulty, mode, score, total_q, started, ended = session
        
        # Format date
        start_date = datetime.strptime(started, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %I:%M %p")
        
        # Calculate score percentage
        score_pct = (score / total_q * 100) if total_q > 0 else 0
        score_color = "#16a34a" if score_pct >= 70 else "#d97706" if score_pct >= 50 else "#dc2626"
        
        with st.expander(f"🎯 {topic} - {difficulty} ({mode}) - {start_date}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="font-family:'Plus Jakarta Sans',sans-serif;">
                    <div style="margin-bottom:12px;">
                        <span style="color:#71717a;font-size:0.85rem;">Score:</span>
                        <span style="color:{score_color};font-weight:600;font-size:1.1rem;margin-left:8px;">
                            {score}/{total_q} ({score_pct:.0f}%)
                        </span>
                    </div>
                    <div style="margin-bottom:12px;">
                        <span style="color:#71717a;font-size:0.85rem;">Duration:</span>
                        <span style="color:#18181b;font-weight:500;margin-left:8px;">
                            {started} to {ended if ended else 'In Progress'}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("View Conversation", key=f"view_{session_id}"):
                    show_conversation(session_id)
    
    if st.button("← Back to Interview", use_container_width=True):
        st.session_state.view_history = False
        st.rerun()

def show_conversation(session_id):
    """Display conversation for a specific session"""
    messages = db.get_session_conversation(session_id)
    
    st.markdown("### Conversation")
    
    for role, content, timestamp in messages:
        with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
            st.markdown(content)
            st.caption(timestamp)
