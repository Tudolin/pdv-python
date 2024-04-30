import csv
import datetime

from flask import Flask, redirect, render_template, request
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__, static_folder='static')

metodo_pagamento = ""
# Dados dos produtos (mesma estrutura do seu código)
data = {}
with open("instance/produtos_export.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data[row['codigo_barras']] = row

def ler_cod(cod_bar):
    item_cod = cod_bar[:7]
    valor = cod_bar[7:]  # Os últimos 7 dígitos representam o valor total
    valor = int(valor)  # Converter para valor em reais (dividir por 100)

    if item_cod[:2] != "20":
        preco = float(data[item_cod][' preco '].replace('R$ ', ''))
        peso = 1
        return data[item_cod]['nome'], peso, preco
    else:
        try:
            item = data[item_cod]
            nome = item['nome']
            preco = float(item[' preco '].replace('R$ ', ''))
            peso = (valor / preco) / 1000
            return nome, peso, preco
        except KeyError:
            raise ValueError("Código de barras inválido")

# Lista para armazenar os itens do carrinho
carrinho = []

@app.route('/', methods=['GET', 'POST'])
def pdv():
    if request.method == 'POST':
        cod_bar = request.form['cod_bar']
        item, peso, preco = ler_cod(cod_bar)
        if item is None:
            return render_template('index.html', error=True)
        
        # Adicionar o item ao carrinho
        carrinho.append((item, peso, preco))
        
        return render_template('index.html', item=item, valor=peso, preco=preco)
    
    return render_template('index.html', error=False)

@app.route('/recibo')
def exibir_recibo():
    total = calcular_total(carrinho)
    recibo = imprimir_recibo(carrinho, total)
    return render_template('recibo.html', recibo=recibo, total=total)

def calcular_total(carrinho):
    total = 0
    for _, valor, preco in carrinho:
        total += valor * preco
    return total

def imprimir_recibo(carrinho, total):
    recibo = []
    for item, _, peso in carrinho:
        valor_item = _ * peso
        recibo.append((item, valor_item, peso))
    return recibo

@app.route('/finalizar', methods=['POST'])
def checkout():

    global metodo_pagamento
    total = calcular_total(carrinho)
    quantia_pg = request.form.get("quantia_pg")
    metodo_pagamento = request.form.get("metodo_pagamento")


    if quantia_pg is not None:
        quantia_pg = float(quantia_pg)
        if quantia_pg == 0:
            troco = 0
        else:
            troco = quantia_pg - total
        return render_template('finalizar.html', total=total, troco=troco)
    else:
        quantia_pg = 0.0
        quantia_pg = float(quantia_pg)
        troco = quantia_pg - total
        return render_template('finalizar.html', total=total, troco=troco)

@app.route('/zerar_carrinho', methods=['POST'])
def finalizar_compra():
    global carrinho 
    carrinho = []
    return redirect('/')

@app.route('/recibo', methods=['POST'])
def imprimir_nf():
    total = calcular_total(carrinho)
    recibo = imprimir_recibo(carrinho, total)
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cpf = request.form.get("cpf") 
    metodo_pagamento = request.form.get("metodo_pagamento")
    return render_template('imprimir_nf.html', recibo=recibo, total=total, data_hora=data_hora, cpf=cpf, metodo_pagamento=metodo_pagamento)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/imprimir_nf', methods=['POST'])
def generate_receipt():
    total = calcular_total(carrinho)
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    teste = request.form.get("cpf")
    if len(teste) < 11:
        teste = teste.zfill(11)
    cpf = '{}.{}.{}-{}'.format(teste[:3], teste[3:6], teste[6:9], teste[9:])
    filename = "receipt.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 700, "Recibo Não Fiscal")
    c.drawString(100, 680, f"Data e Hora: {data_hora}")
    c.drawString(100, 660, f"CPF: {cpf}")

    # Adicione os itens comprados ao recibo
    y = 640

    c.drawString(100, y, f"Total: R$ {total:.2f}")
    c.save()

    return f"Recibo gerado com sucesso! Verifique o arquivo {filename}."

@app.route('/recibo', methods=['POST'])
def imprimir_nf():
    total = calcular_total(carrinho)
    recibo = imprimir_recibo(carrinho, total)
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cpf = request.form.get("cpf")  # Se o CPF foi incluído no formulário

    # Renderizando o recibo não fiscal
    return render_template('imprimir_nf.html', recibo=recibo, total=total, data_hora=data_hora, cpf=cpf)

if __name__ == '__main__':
    app.run(debug=True)