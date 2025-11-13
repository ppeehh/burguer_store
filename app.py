from flask import Flask, render_template, request, redirect, url_for, session
import json
import urllib.parse

app = Flask(__name__)
app.secret_key = 'seu_segredo_aqui'

# Carrega os produtos do cardápio
with open('produtos.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    nome = request.form['nome']
    mensagem = request.form['mensagem']
    resposta = f"Olá {nome}! 😄 Clique no link abaixo para ver nosso cardápio:\n\nhttp://localhost:5000/cardapio"
    return render_template('index.html', resposta=resposta)

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html', produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    item = request.form['produto']
    preco = float(request.form['preco'])
    
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append({'produto': item, 'preco': preco})
    session.modified = True
    return redirect(url_for('cardapio'))

@app.route('/confirmar')
def confirmar():
    carrinho = session.get('carrinho', [])
    total = sum(item['preco'] for item in carrinho)
    return render_template('confirmar.html', carrinho=carrinho, total=total)

@app.route('/enviar_pedido', methods=['POST'])
def enviar_pedido():
    nome = request.form['nome']
    endereco = request.form['endereco']
    carrinho = session.get('carrinho', [])
    
    texto_pedido = f"🍔 *Novo pedido de {nome}*\n\n"
    for item in carrinho:
        texto_pedido += f"- {item['produto']} (R${item['preco']:.2f})\n"
    texto_pedido += f"\n📍 Endereço: {endereco}"
    
    texto_codificado = urllib.parse.quote(texto_pedido)
    numero_whatsapp = "5511987835856"  # número do restaurante (com DDI 55)
    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={texto_codificado}"

    session.pop('carrinho', None)
    return redirect(link_whatsapp)

if __name__ == '__main__':
    app.run(debug=True)
