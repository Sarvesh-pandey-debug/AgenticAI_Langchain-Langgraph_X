import sqlite3

db = sqlite3.connect('chatbot_memory.db')
c = db.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", c.fetchall())

c.execute("PRAGMA table_info(checkpoints)")
print("Columns:", c.fetchall())

c.execute("SELECT DISTINCT thread_id FROM checkpoints LIMIT 10")
print("Threads:", c.fetchall())

db.close()
