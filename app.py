from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ======================
# BANCO
# ======================

def init_db():
    conn = sqlite3.connect("mocha.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        categoria TEXT,
        dificuldade TEXT,
        xp INTEGER,
        status TEXT DEFAULT 'pendente'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progresso (
        id INTEGER PRIMARY KEY,
        xp_total INTEGER,
        streak INTEGER
    )
    """)

    cursor.execute("SELECT * FROM progresso WHERE id=1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO progresso VALUES (1,0,0)")

    conn.commit()
    conn.close()

init_db()

# ======================
# HOME
# ======================

@app.route("/")
def index():
    conn = sqlite3.connect("mocha.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tarefas ORDER BY id DESC")
    tarefas = cursor.fetchall()

    cursor.execute("SELECT xp_total, streak FROM progresso WHERE id=1")
    xp_total, streak = cursor.fetchone()

    nivel = xp_total // 100
    xp_nivel = xp_total % 100

    conn.close()

    return render_template(
        "index.html",
        tarefas=tarefas,
        xp_total=xp_total,
        nivel=nivel,
        xp_nivel=xp_nivel,
        streak=streak
    )

# ======================
# NOVA TAREFA
# ======================

@app.route("/nova_tarefa", methods=["POST"])
def nova_tarefa():
    titulo = request.form["titulo"]
    categoria = request.form["categoria"]
    dificuldade = request.form["dificuldade"]

    xp_map = {"facil": 10, "media": 20, "dificil": 30}
    xp = xp_map[dificuldade]

    conn = sqlite3.connect("mocha.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tarefas (titulo, categoria, dificuldade, xp)
        VALUES (?, ?, ?, ?)
    """, (titulo, categoria, dificuldade, xp))

    conn.commit()
    conn.close()

    return redirect("/")

# ======================
# CONCLUIR
# ======================

@app.route("/concluir/<int:id>")
def concluir(id):
    conn = sqlite3.connect("mocha.db")
    cursor = conn.cursor()

    cursor.execute("SELECT xp FROM tarefas WHERE id=?", (id,))
    xp = cursor.fetchone()[0]

    cursor.execute("UPDATE tarefas SET status='concluida' WHERE id=?", (id,))
    cursor.execute("UPDATE progresso SET xp_total = xp_total + ?, streak = streak + 1 WHERE id=1", (xp,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
