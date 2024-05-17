import csv
import json
import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__, static_folder='static')

metodo_pagamento = ""
data = {}
with open("instance/produtos_export.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data[row['codigo_barras']] = row

def ler_cod(cod_bar):
    valor = cod_bar[7:]  
    valor = int(valor)
    item_cod = cod_bar
    if item_cod[:2] != "20":
        preco = float(data[item_cod][' preco '].replace('R$ ', ''))
        peso = 1
        return data[item_cod]['nome'], peso, preco
    if item_cod[:6] == "2000000":
        preco = 1
        peso = 1
        return data[item_cod]['nome'], peso, preco
    else:
        try:
            item_cod = item_cod[:7]
            item = data[item_cod]
            nome = item['nome']
            preco = float(item[' preco '].replace('R$ ', ''))
            peso = (valor / preco) / 1000
            return nome, peso, preco
        except KeyError:
            raise ValueError("Código de barras inválido")

def adicionar_venda(carrinho, total, cpf):
    try:
        with open('vendas.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"vendas": []}

    venda = {
        datetime.now().strftime("%d-%m-%Y"): {
            "valor": round(total, 2),
            "cpf": cpf,
            "itens": {i: {"nome": item, "peso": round(valor_item, 3)} for i, (item, valor_item, _) in enumerate(carrinho, start=1)}
        }
    }

    data["vendas"].append(venda)

    with open('vendas.json', 'w') as f:
        json.dump(data, f, indent=4)

carrinho = []

def print_pdf(filename):
    print_command = f"print /d:my_printer {filename}"
    os.system(print_command)

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

@app.route('/delete/<item>', methods=['POST'])
def delete_item(item):
    global carrinho
    carrinho = [i for i in carrinho if i[0] != item]
    return redirect(url_for('exibir_recibo'))

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


# Utilizando o caminho /recibo, declarada em 'finalizar.html', gerara uma webpage com o recibo.
@app.route('/recibo', methods=['POST'])
def imprimir_nf():
    total = calcular_total(carrinho)
    recibo = imprimir_recibo(carrinho, total)
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cpf = request.form.get("cpf") 
    metodo_pagamento = request.form.get("metodo_pagamento")
    adicionar_venda(carrinho, total, cpf)

    return render_template('imprimir_nf.html', recibo=recibo, total=total, data_hora=data_hora, cpf=cpf, metodo_pagamento=metodo_pagamento)

# Utilizando o caminho /gerar_recibo, declarada em 'finalizar.html', gerara um pdf com o recibo.
@app.route('/gerar_recibo', methods=['POST'])
def generate_receipt():
    total = calcular_total(carrinho)
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cpf = request.form.get("cpf")
    filename = "receipt.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    y = 750
    c.drawString(100, y, "Recibo Não Fiscal")
    y -= 20
    c.drawString(100, y, "-----------------------------------------")
    y -= 20
    c.drawString(100, y, "Casa das Massas Pinheirinho - (41) 3268-2817")
    y -= 15
    c.drawString(100, y, "Rua Mário Gomes Cezar - Nº230 - Pinheirinho")
    y -= 15
    c.drawString(100, y, f"Data e Hora: {data_hora}")
    y -= 15
    c.drawString(100, y, "-----------------------------------------")
    y -= 20

    for item, valor_item, peso in carrinho:
        c.drawString(100, y, f"Peso : {valor_item:.3f} Kg | {item} Preço por KG / Unidade {peso} | Valor : R$ {(peso * valor_item):.2f}")
        y -= 20
    c.drawString(100, y, "-----------------------------------------")
    y -= 20
    c.drawString(100, y, f"Total: R$ {total:.2f}")
    y -= 10
    c.drawString(100, y, f"CPF: {cpf}")
    y -= 20
    c.drawString(100, y, "-----------------------------------------")
    y -= 20
    c.drawString(100, y, "Parabéns, você acaba de comprar a melhor massa da região!!")
    y -= 10
    c.drawString(100, y, "Muito obrigado pela preferencia, volte sempre c:")

    c.save()

    print_pdf('receipt.pdf')

    adicionar_venda(carrinho, total, cpf)

    return f"Recibo gerado com sucesso! Verifique o arquivo {filename}."


if __name__ == '__main__':
    app.run(debug=True)