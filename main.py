from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Faculty Finder API")


def get_db_connection():
    conn = sqlite3.connect("faculty.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def root():
    return {"message": "Faculty Finder API is running"}


@app.get("/faculty")
def get_all_faculty():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/faculty/type/{faculty_type}")
def get_faculty_by_type(faculty_type: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    if faculty_type.lower() == "faculty":
        cursor.execute("SELECT * FROM faculty")
    else:
        cursor.execute(
            "SELECT * FROM faculty WHERE faculty_type = ?",
            (faculty_type.lower(),)
        )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/faculty/{faculty_id}")
def get_faculty_by_id(faculty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM faculty WHERE id = ?",
        (faculty_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"error": "Faculty not found"}

    return dict(row)


