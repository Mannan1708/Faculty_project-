import sqlite3

conn = sqlite3.connect("faculty.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, name, faculty_type, email
FROM faculty
LIMIT 5
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
