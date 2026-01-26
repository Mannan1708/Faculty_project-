import json
import sqlite3

with open("faculty_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Records loaded:", len(data))


conn = sqlite3.connect("faculty.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_type TEXT,
    name TEXT,
    education TEXT,
    phone TEXT,
    address TEXT,
    email TEXT,
    specialization TEXT
)
""")

print("Database and table ready")

for faculty in data:
    cursor.execute("""
        INSERT INTO faculty (
            faculty_type,
            name,
            education,
            phone,
            address,
            email,
            specialization
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        faculty.get("faculty_type"),
        faculty.get("name"),
        faculty.get("education"),
        faculty.get("phone"),
        faculty.get("address"),
        faculty.get("email"),
        faculty.get("specialization")
    ))

conn.commit()
print("Data inserted into database")





print("I AM AT THE END OF THE FILE")
