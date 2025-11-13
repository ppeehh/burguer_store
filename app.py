from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "troque_essa_chave_antes_de_publicar"

ADMIN_PASSWORD = "burguer1234"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- BANCO DE DADOS ---
def init_db():
    with sqlite3.connect("burguer_store.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                categoria TEXT NOT NULL,
                imagem TEXT
            )
        """)

init_db()

def get_db_connection():
    conn = sqlite3.connect("burguer_store.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- ROTAS ---
@app.route("/")
def index():
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()

    # Agrupa por categoria
    categorias = {}
    for p in produtos:
        cat = p["categoria"] if p["categoria"] else "Outros"
        categorias.setdefault(cat, []).append(p)

    return render_template("cardapio.html", produtos=categorias)

# --- LOGIN ADMIN SECRETO (3 cliques) ---
@app.route("/admin123", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha", "")
        if senha == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            flash("Senha inválida!", "error")
    return render_template("login.html")

# --- PAINEL ADMIN ---
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("index"))
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return render_template("painel.html", produtos=produtos)

# --- ADICIONAR PRODUTO ---
@app.route("/add", methods=["POST"])
def add_produto():
    if not session.get("admin"):
        return redirect(url_for("index"))

    nome = request.form["nome"]
    descricao = request.form.get("descricao", "")
    preco = request.form["preco"]
    categoria = request.form["categoria"]
    imagem = request.files["imagem"]

    if imagem:
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        imagem_path = f"uploads/{filename}"
    else:
        imagem_path = ""

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO produtos (nome, descricao, preco, categoria, imagem) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, categoria, imagem_path)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

# --- DELETAR PRODUTO ---
@app.route("/delete/<int:id>")
def delete_produto(id):
    if not session.get("admin"):
        return redirect(url_for("index"))
    conn = get_db_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

# --- LOGOUT ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
