from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")

    if task:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (task,)
        )

        conn.commit()
        conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)