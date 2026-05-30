import sqlite3
from datetime import datetime

conn = sqlite3.connect('database/interview_ai.db')
cursor = conn.cursor()

# Check current database time
cursor.execute('SELECT datetime("now", "localtime")')
print('Current DB time:', cursor.fetchone()[0])

# Check total messages
cursor.execute('SELECT COUNT(*) FROM conversation_history')
print('Total messages in history:', cursor.fetchone()[0])

# Check recent sessions
cursor.execute('''
    SELECT id, user_id, topic, difficulty, mode, started_at, ended_at
    FROM interview_sessions
    ORDER BY started_at DESC
    LIMIT 5
''')
print('\nRecent sessions:')
for row in cursor.fetchall():
    print(f"  Session {row[0]}: User {row[1]}, {row[2]} ({row[3]}), Started: {row[5]}, Ended: {row[6]}")

# Check recent messages
cursor.execute('''
    SELECT session_id, role, substr(content, 1, 50), timestamp
    FROM conversation_history
    ORDER BY timestamp DESC
    LIMIT 10
''')
print('\nRecent messages:')
for row in cursor.fetchall():
    print(f"  Session {row[0]}, {row[1]}: {row[2]}... at {row[3]}")

# Check if there are any sessions without messages
cursor.execute('''
    SELECT s.id, s.topic, s.started_at, COUNT(c.id) as msg_count
    FROM interview_sessions s
    LEFT JOIN conversation_history c ON s.id = c.session_id
    GROUP BY s.id
    ORDER BY s.started_at DESC
    LIMIT 10
''')
print('\nSessions with message counts:')
for row in cursor.fetchall():
    print(f"  Session {row[0]} ({row[1]}): {row[3]} messages, Started: {row[2]}")

conn.close()
