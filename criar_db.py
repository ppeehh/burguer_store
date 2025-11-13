import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    categoria TEXT NOT NULL,
    imagem TEXT
)
''')

# Inserir exemplos se tabela estiver vazia
cur.execute('SELECT COUNT(*) FROM produtos')
if cur.fetchone()[0] == 0:
    exemplos = [
        ("X-Burger","Hambúrguer artesanal com queijo e molho especial",15.90,"Lanches","xburger.jpg"),
        ("X-Salada","Hambúrguer com salada fresca",17.50,"Lanches","xsalada.jpg"),
        ("Refrigerante Lata","Coca/Guaraná/Fanta 350ml",6.00,"Bebidas","refri.jpg"),
        ("Suco Natural","Suco 500ml",8.00,"Bebidas","suco.jpg")
    ]
    cur.executemany('INSERT INTO produtos (nome, descricao, preco, categoria, imagem) VALUES (?, ?, ?, ?, ?)', exemplos)

conn.commit()
conn.close()
print("Banco criado/atualizado com sucesso.")
