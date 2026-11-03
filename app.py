from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
DB_PATH = Path(__file__).with_name("techmanager.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            requester TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Média',
            status TEXT NOT NULL DEFAULT 'Aberto',
            description TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            tag TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Em uso'
        );
        """)
        if db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 0:
            db.execute("""INSERT INTO tickets
                (title, requester, category, priority, status, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                ("Computador não inicia", "Mariana Costa", "Hardware", "Alta", "Em andamento",
                 "Estação de trabalho não liga após queda de energia.", datetime.now().strftime("%d/%m/%Y")))
            db.execute("""INSERT INTO tickets
                (title, requester, category, priority, status, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                ("Solicitação de acesso ao sistema", "João Pedro", "Acesso", "Média", "Aberto",
                 "Usuário precisa de acesso ao sistema interno.", datetime.now().strftime("%d/%m/%Y")))
        if db.execute("SELECT COUNT(*) FROM assets").fetchone()[0] == 0:
            db.execute("""INSERT INTO assets (name, asset_type, tag, department, status)
                          VALUES (?, ?, ?, ?, ?)""",
                       ("Notebook Dell Latitude", "Notebook", "PAT-001", "Administrativo", "Em uso"))
            db.execute("""INSERT INTO assets (name, asset_type, tag, department, status)
                          VALUES (?, ?, ?, ?, ?)""",
                       ("Impressora HP LaserJet", "Impressora", "PAT-002", "Financeiro", "Em manutenção"))

@app.route("/")
def dashboard():
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        open_count = db.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Aberto'").fetchone()[0]
        progress = db.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Em andamento'").fetchone()[0]
        resolved = db.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Concluído'").fetchone()[0]
        assets = db.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
        recent = db.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("dashboard.html", total=total, open_count=open_count,
                           progress=progress, resolved=resolved, assets=assets, recent=recent)

@app.route("/chamados")
def tickets():
    with get_db() as db:
        rows = db.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    return render_template("tickets.html", tickets=rows)

@app.route("/chamados/novo", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        requester = request.form.get("requester", "").strip()
        category = request.form.get("category", "")
        priority = request.form.get("priority", "Média")
        description = request.form.get("description", "").strip()
        if not title or not requester or not category:
            flash("Preencha título, solicitante e categoria.", "error")
            return render_template("ticket_form.html")
        with get_db() as db:
            db.execute("""INSERT INTO tickets
                (title, requester, category, priority, status, description, created_at)
                VALUES (?, ?, ?, ?, 'Aberto', ?, ?)""",
                (title, requester, category, priority, description, datetime.now().strftime("%d/%m/%Y")))
        flash("Chamado cadastrado com sucesso!", "success")
        return redirect(url_for("tickets"))
    return render_template("ticket_form.html")

@app.post("/chamados/<int:ticket_id>/status")
def update_ticket(ticket_id):
    status = request.form.get("status")
    if status not in ["Aberto", "Em andamento", "Concluído"]:
        flash("Status inválido.", "error")
        return redirect(url_for("tickets"))
    with get_db() as db:
        db.execute("UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id))
    flash("Status do chamado atualizado.", "success")
    return redirect(url_for("tickets"))

@app.route("/ativos")
def assets():
    with get_db() as db:
        rows = db.execute("SELECT * FROM assets ORDER BY id DESC").fetchall()
    return render_template("assets.html", assets=rows)

@app.route("/ativos/novo", methods=["GET", "POST"])
def new_asset():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        asset_type = request.form.get("asset_type", "")
        tag = request.form.get("tag", "").strip().upper()
        department = request.form.get("department", "").strip()
        if not all([name, asset_type, tag, department]):
            flash("Preencha todos os campos.", "error")
            return render_template("asset_form.html")
        try:
            with get_db() as db:
                db.execute("""INSERT INTO assets (name, asset_type, tag, department)
                              VALUES (?, ?, ?, ?)""", (name, asset_type, tag, department))
            flash("Ativo cadastrado com sucesso!", "success")
            return redirect(url_for("assets"))
        except sqlite3.IntegrityError:
            flash("Já existe um ativo com esse número de patrimônio.", "error")
    return render_template("asset_form.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
