from datetime import datetime
from database.db_manager import create_session, save_message, get_user_sessions
import sys

# Test timestamp storage
print("Current local time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Testing database timestamp storage...")

# Create a test session (assuming user_id 1 exists)
try:
    session_id = create_session(1, "Python", "Intermediate", "Text")
    print(f"Created session ID: {session_id}")
    
    # Save a test message
    save_message(session_id, "assistant", "Test message")
    print("Saved test message")
    
    # Retrieve and check timestamp
    sessions = get_user_sessions(1, limit=1)
    if sessions:
        latest = sessions[0]
        print(f"Retrieved timestamp: {latest[6]}")  # started_at is index 6
        print("✅ Timestamp matches local time!" if latest[6].startswith(datetime.now().strftime("%Y-%m-%d")) else "❌ Timestamp is wrong!")
    else:
        print("No sessions found")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
