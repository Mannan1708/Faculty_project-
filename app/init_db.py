import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "faculty.db")
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "faculty_clean.json")

def init_db():
    if os.path.exists(DB_PATH):
        print("Database already exists. Skipping initialization.")
        return

    print("Initializing database from backup JSON...")
    
    if not os.path.exists(JSON_PATH):
        print("Error: faculty_clean.json not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
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
    ''')

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Loaded {len(data)} records from JSON.")
        
        count = 0
        for item in data:
            cursor.execute('''
                INSERT INTO faculty (faculty_type, name, education, phone, address, email, specialization)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('faculty_type'),
                item.get('name'),
                item.get('education'),
                item.get('phone'),
                item.get('address'),
                item.get('email'),
                item.get('specialization')
            ))
            count += 1
            
        conn.commit()
        print(f"Successfully inserted {count} records into faculty.db")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
