from .database import get_db_connection

def get_faculty(id: int):
    conn = get_db_connection()
    faculty = conn.execute('SELECT * FROM faculty WHERE id = ?', (id,)).fetchone()
    conn.close()
    return dict(faculty) if faculty else None

def get_all_faculty(skip: int = 0, limit: int = 20):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM faculty LIMIT ? OFFSET ?', (limit, skip)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def search_faculty(query: str):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM faculty WHERE name LIKE ? OR specialization LIKE ? OR education LIKE ?",
        (f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
