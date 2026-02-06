import sqlite3
import pandas as pd

def inspect_db():
    conn = sqlite3.connect('faculty.db')
    cursor = conn.cursor()
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    for table_info in tables:
        table_name = table_info[0]
        print(f"\n--- Table: {table_name} ---")
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
        print(df.columns.tolist())
        print(df.head(1).to_dict('records'))
    
    conn.close()

if __name__ == "__main__":
    inspect_db()
