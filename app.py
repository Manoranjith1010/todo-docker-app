from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "notes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    search = request.args.get("search", "")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cursor.execute("SELECT * FROM notes ORDER BY id DESC")

    notes = cursor.fetchall()

    conn.close()

    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    content = request.form.get("content")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (title, content, created_at)
        VALUES (?, ?, ?)
    """, (
        title,
        content,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        cursor.execute("""
            UPDATE notes
            SET title=?, content=?
            WHERE id=?
        """, (title, content, id))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM notes WHERE id=?", (id,))
    note = cursor.fetchone()

    conn.close()

    return render_template("edit.html", note=note)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)