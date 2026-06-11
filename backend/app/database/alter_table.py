import sqlite3

conn = sqlite3.connect(
    "evopoint.db"
)

cursor = conn.cursor()

cursor.execute("""

ALTER TABLE settings
ADD COLUMN last_log_index INTEGER DEFAULT 0

""")

conn.commit()

print("COLUNA CRIADA")

conn.close()