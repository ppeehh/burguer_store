from flask import Flask, render_template, json

app = Flask(__name__)

@app.route('/')
def cardapio():
    # carrega produtos.json
    with open('produtos.json', encoding='utf-8') as f:
        produtos = json.load(f)
    return render_template('cardapio.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
