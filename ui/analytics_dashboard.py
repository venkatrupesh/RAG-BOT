# AI Performance Analytics Component
import streamlit as st
import json
from datetime import datetime

def render_analytics_dashboard(user_id, get_user_sessions_fn, ask_groq_fn):
    """Render AI-powered performance analytics dashboard with REAL user data"""
    
    # Professional Header
    st.markdown(
        "<div style='margin-bottom:2rem;'>" 
        "<h1 style='font-size:2rem; font-weight:700; color:#111827; margin:0 0 0.5rem 0; letter-spacing:-0.02em;'>Performance Analytics</h1>"
        "<p style='color:#6b7280; font-size:0.95rem; margin:0;'>Data-driven insights from your interview sessions</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Get REAL user sessions from database
    sessions = get_user_sessions_fn(user_id, limit=100)
    
    if not sessions:
        st.markdown(
            "<div style='text-align:center; padding:4rem 2rem; background:#f9fafb; border-radius:16px; border:2px dashed #e5e7eb;'>"
            "<div style='font-size:3rem; margin-bottom:1rem;'>📊</div>"
            "<h3 style='color:#111827; margin-bottom:0.5rem;'>No Data Yet</h3>"
            "<p style='color:#6b7280; margin-bottom:2rem;'>Complete interviews to unlock analytics</p>"
            "<div style='display:inline-block; text-align:left; background:#ffffff; padding:1.5rem; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.1);'>"
            "<div style='color:#374151; font-size:0.9rem; line-height:1.8;'>"
            "<div style='margin-bottom:0.5rem;'>✓ Strengths & Weaknesses Analysis</div>"
            "<div style='margin-bottom:0.5rem;'>✓ Performance Trends Over Time</div>"
            "<div style='margin-bottom:0.5rem;'>✓ Personalized AI Recommendations</div>"
            "<div style='margin-bottom:0.5rem;'>✓ Topic Mastery Tracking</div>"
            "<div>✓ Progress Visualization</div>"
            "</div></div></div>",
            unsafe_allow_html=True
        )
        return
    
    # Filter only sessions with actual scores (completed interviews)
    completed_sessions = [s for s in sessions if s[5] and s[5] > 0]
    
    if not completed_sessions:
        st.markdown(
            f"<div style='background:#fffbeb; border:1px solid #fcd34d; border-radius:12px; padding:1.5rem; text-align:center;'>"
            f"<div style='font-size:2rem; margin-bottom:0.5rem;'>⏳</div>"
            f"<div style='color:#92400e; font-weight:600; margin-bottom:0.5rem;'>Incomplete Sessions</div>"
            f"<div style='color:#78350f; font-size:0.9rem;'>You have {len(sessions)} started interview(s). Complete them to see analytics.</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        return
    
    # Calculate REAL statistics from user's actual data
    total_interviews = len(completed_sessions)
    total_questions = sum(s[5] for s in completed_sessions)
    total_correct = sum(s[4] for s in completed_sessions)
    
    # Overall accuracy from REAL data
    overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # Topic-wise performance from REAL user data
    topic_stats = {}
    for session in completed_sessions:
        topic = session[1]
        score = session[4]
        total = session[5]
        
        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0, "count": 0}
        
        topic_stats[topic]["correct"] += score
        topic_stats[topic]["total"] += total
        topic_stats[topic]["count"] += 1
    
    # Difficulty-wise performance from REAL user data
    difficulty_stats = {}
    for session in completed_sessions:
        diff = session[2]
        score = session[4]
        total = session[5]
        
        if diff not in difficulty_stats:
            difficulty_stats[diff] = {"correct": 0, "total": 0}
        
        difficulty_stats[diff]["correct"] += score
        difficulty_stats[diff]["total"] += total
    
    # Modern Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"<div style='background:#ffffff; padding:1.5rem; border-radius:12px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>"
            f"<div style='color:#6b7280; font-size:0.8rem; font-weight:500; margin-bottom:0.75rem;'>Total Interviews</div>"
            f"<div style='color:#111827; font-size:2.25rem; font-weight:700; margin-bottom:0.25rem;'>{total_interviews}</div>"
            f"<div style='color:#10b981; font-size:0.75rem; font-weight:500;'>● Active</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"<div style='background:#ffffff; padding:1.5rem; border-radius:12px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>"
            f"<div style='color:#6b7280; font-size:0.8rem; font-weight:500; margin-bottom:0.75rem;'>Questions Answered</div>"
            f"<div style='color:#111827; font-size:2.25rem; font-weight:700; margin-bottom:0.25rem;'>{total_questions}</div>"
            f"<div style='color:#3b82f6; font-size:0.75rem; font-weight:500;'>● Completed</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"<div style='background:#ffffff; padding:1.5rem; border-radius:12px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>"
            f"<div style='color:#6b7280; font-size:0.8rem; font-weight:500; margin-bottom:0.75rem;'>Overall Accuracy</div>"
            f"<div style='color:#111827; font-size:2.25rem; font-weight:700; margin-bottom:0.25rem;'>{overall_accuracy:.0f}%</div>"
            f"<div style='color:#8b5cf6; font-size:0.75rem; font-weight:500;'>● Performance</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    with col4:
        recent_sessions = completed_sessions[:5]
        streak = sum(1 for s in recent_sessions if (s[4]/s[5]) >= 0.7)
        
        st.markdown(
            f"<div style='background:#ffffff; padding:1.5rem; border-radius:12px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>"
            f"<div style='color:#6b7280; font-size:0.8rem; font-weight:500; margin-bottom:0.75rem;'>Current Streak</div>"
            f"<div style='color:#111827; font-size:2.25rem; font-weight:700; margin-bottom:0.25rem;'>{streak} 🔥</div>"
            f"<div style='color:#f59e0b; font-size:0.75rem; font-weight:500;'>● Consistency</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
    
    # Topic Mastery Section
    st.markdown(
        "<div style='margin-bottom:1.5rem;'>"
        "<h2 style='font-size:1.25rem; font-weight:600; color:#111827; margin:0 0 0.5rem 0;'>Topic Mastery</h2>"
        "<p style='color:#6b7280; font-size:0.85rem; margin:0;'>Your performance across different topics</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    for topic, stats in topic_stats.items():
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            
            if accuracy >= 80:
                level = "Expert"
                badge_color = "#10b981"
                bg_color = "#f0fdf4"
            elif accuracy >= 60:
                level = "Proficient"
                badge_color = "#3b82f6"
                bg_color = "#eff6ff"
            elif accuracy >= 40:
                level = "Learning"
                badge_color = "#f59e0b"
                bg_color = "#fffbeb"
            else:
                level = "Beginner"
                badge_color = "#ef4444"
                bg_color = "#fef2f2"
            
            st.markdown(
                f"<div style='background:#ffffff; padding:1.25rem; border-radius:12px; margin-bottom:1rem; border:1px solid #e5e7eb; box-shadow:0 1px 2px rgba(0,0,0,0.05);'>"
                f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;'>"
                f"<div style='font-weight:600; color:#111827; font-size:1rem;'>{topic}</div>"
                f"<div style='background:{bg_color}; color:{badge_color}; padding:0.25rem 0.75rem; border-radius:6px; font-size:0.8rem; font-weight:600;'>{level}</div>"
                f"</div>"
                f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;'>"
                f"<span style='color:#6b7280; font-size:0.85rem;'>{stats['count']} interviews • {stats['correct']}/{stats['total']} correct</span>"
                f"<span style='color:#111827; font-weight:700; font-size:1.1rem;'>{accuracy:.0f}%</span>"
                f"</div>"
                f"<div style='background:#f3f4f6; height:8px; border-radius:4px; overflow:hidden;'>"
                f"<div style='background:{badge_color}; height:100%; width:{accuracy}%; border-radius:4px; transition:width 0.3s;'></div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
    
    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
    
    # Difficulty Analysis Section
    st.markdown(
        "<div style='margin-bottom:1.5rem;'>"
        "<h2 style='font-size:1.25rem; font-weight:600; color:#111827; margin:0 0 0.5rem 0;'>Difficulty Breakdown</h2>"
        "<p style='color:#6b7280; font-size:0.85rem; margin:0;'>Performance across difficulty levels</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    diff_cols = st.columns(3)
    diff_config = {
        "Beginner": {"icon": "🟢", "color": "#10b981", "bg": "#f0fdf4"},
        "Intermediate": {"icon": "🟡", "color": "#f59e0b", "bg": "#fffbeb"},
        "Advanced": {"icon": "🔴", "color": "#ef4444", "bg": "#fef2f2"}
    }
    
    for idx, (diff, stats) in enumerate(difficulty_stats.items()):
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            config = diff_config.get(diff, {"icon": "⚪", "color": "#6b7280", "bg": "#f9fafb"})
            
            with diff_cols[idx % 3]:
                st.markdown(
                    f"<div style='background:#ffffff; padding:1.5rem; border-radius:12px; text-align:center; border:1px solid #e5e7eb; box-shadow:0 1px 2px rgba(0,0,0,0.05);'>"
                    f"<div style='background:{config['bg']}; width:56px; height:56px; border-radius:12px; margin:0 auto 1rem; display:flex; align-items:center; justify-content:center; font-size:1.75rem;'>{config['icon']}</div>"
                    f"<div style='font-weight:600; color:#111827; margin-bottom:0.75rem; font-size:0.95rem;'>{diff}</div>"
                    f"<div style='font-size:2rem; font-weight:700; color:{config['color']}; margin-bottom:0.5rem;'>{accuracy:.0f}%</div>"
                    f"<div style='color:#6b7280; font-size:0.8rem;'>{stats['correct']} of {stats['total']} correct</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    
    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
    
    # AI Insights Section
    st.markdown(
        "<div style='margin-bottom:1.5rem;'>"
        "<h2 style='font-size:1.25rem; font-weight:600; color:#111827; margin:0 0 0.5rem 0;'>AI-Powered Insights</h2>"
        "<p style='color:#6b7280; font-size:0.85rem; margin:0;'>Get personalized recommendations based on your performance</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    if st.button("✨ Generate Insights", use_container_width=True, type="primary"):
        with st.spinner("Analyzing your performance..."):
            try:
                # Prepare REAL user data for AI analysis
                analysis_data = {
                    "total_interviews": total_interviews,
                    "total_questions": total_questions,
                    "total_correct": total_correct,
                    "overall_accuracy": round(overall_accuracy, 1),
                    "topic_performance": {
                        topic: {
                            "accuracy": round((stats["correct"] / stats["total"] * 100), 1),
                            "interviews_completed": stats["count"],
                            "questions_answered": stats["total"],
                            "correct_answers": stats["correct"]
                        }
                        for topic, stats in topic_stats.items()
                    },
                    "difficulty_performance": {
                        diff: {
                            "accuracy": round((stats["correct"] / stats["total"] * 100), 1),
                            "questions_answered": stats["total"],
                            "correct_answers": stats["correct"]
                        }
                        for diff, stats in difficulty_stats.items()
                    },
                    "current_streak": streak
                }
                
                prompt = f"""Analyze this REAL interview performance data and provide personalized insights:

{json.dumps(analysis_data, indent=2)}

This is ACTUAL user data from completed interviews. Provide detailed analysis:

1. **🎯 Key Strengths** - What they're genuinely doing well based on actual scores
2. **⚠️ Areas for Improvement** - Specific weaknesses from real performance
3. **💡 Actionable Recommendations** - 3-5 personalized steps based on weak areas
4. **🎓 Learning Path** - Topics to focus on based on current mastery
5. **🏆 Achievement Recognition** - Celebrate real accomplishments

Be specific, data-driven, encouraging. Reference actual numbers. Use emojis."""

                response = ask_groq_fn(
                    "You are an expert technical interview coach analyzing REAL user performance data.",
                    [{"role": "user", "content": prompt}]
                )
                
                st.markdown(
                    f"<div style='background:#ffffff; padding:2rem; border-radius:12px; border:1px solid #e5e7eb; box-shadow:0 4px 6px rgba(0,0,0,0.05);'>"
                    f"<div style='color:#111827; line-height:1.7;'>{response}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
    
    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
    
    # Recent Activity Section
    st.markdown(
        f"<div style='margin-bottom:1.5rem;'>"
        f"<h2 style='font-size:1.25rem; font-weight:600; color:#111827; margin:0 0 0.5rem 0;'>Recent Activity</h2>"
        f"<p style='color:#6b7280; font-size:0.85rem; margin:0;'>Last {min(10, len(completed_sessions))} completed interviews</p>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    for session in completed_sessions[:10]:
        session_id, topic, difficulty, mode, score, total, start_time, end_time = session
        
        if total and total > 0:
            accuracy = (score / total) * 100
            
            try:
                start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                formatted_time = start_dt.strftime("%b %d, %Y • %I:%M %p")
            except:
                formatted_time = str(start_time)[:16]
            
            if accuracy >= 70:
                status_color = "#10b981"
                status_bg = "#f0fdf4"
                status_text = "Excellent"
            elif accuracy >= 50:
                status_color = "#f59e0b"
                status_bg = "#fffbeb"
                status_text = "Good"
            else:
                status_color = "#ef4444"
                status_bg = "#fef2f2"
                status_text = "Needs Work"
            
            st.markdown(
                f"<div style='background:#ffffff; padding:1.25rem; border-radius:12px; margin-bottom:0.75rem; border:1px solid #e5e7eb; box-shadow:0 1px 2px rgba(0,0,0,0.05);'>"
                f"<div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;'>"
                f"<div>"
                f"<div style='font-weight:600; color:#111827; margin-bottom:0.25rem;'>{topic}</div>"
                f"<div style='color:#6b7280; font-size:0.8rem;'>{difficulty} • {mode}</div>"
                f"</div>"
                f"<div style='background:{status_bg}; color:{status_color}; padding:0.25rem 0.75rem; border-radius:6px; font-size:0.75rem; font-weight:600;'>{status_text}</div>"
                f"</div>"
                f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
                f"<span style='color:#6b7280; font-size:0.8rem;'>{formatted_time}</span>"
                f"<span style='color:#111827; font-weight:600;'>{score}/{total} <span style='color:#6b7280;'>({accuracy:.0f}%)</span></span>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )
