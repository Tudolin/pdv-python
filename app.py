from flask import (Flask, current_app, redirect, render_template, request,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurante.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(100), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tipo_unidade = db.Column(db.String(10), nullable=False)  # 'KG' ou 'UNIDADE'
    codigo_barras = db.Column(db.Integer, nullable = True)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itens = db.relationship('ItemVenda', backref='venda', lazy=True)
    total = db.Column(db.Float, nullable=False)
    metodo_pagamento = db.Column(db.String(50), nullable=False)

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('pdv.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        
        # Verifique se o nome de usuário já existe
        usuario_existente = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        if usuario_existente:
            return 'Nome de usuário já está em uso. Escolha outro nome.'
        
        # Crie um novo usuário
        novo_usuario = Usuario(nome_usuario=nome_usuario, senha_hash=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return 'Cadastro realizado com sucesso!'
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session['usuario_logado'] = usuario.nome_usuario
            return redirect(url_for('index'))
        return 'Login falhou!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

@app.route('/vendas', methods=['GET'])
def vendas():
    if request.method == 'GET':
        todas_vendas = Venda.query.all()
        return render_template('vendas.html', vendas=todas_vendas)
    
@app.route('/itens')
def listar_itens():
    todos_itens = Item.query.all()
    return render_template('itens.html', itens=todos_itens)

@app.route('/itens/novo', methods=['GET', 'POST'])
def novo_item():
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']
        preco = request.form['preco']
        tipo_unidade = request.form['tipo_unidade']
        codigo_barras = request.form['codigo_barras']
        novo_item = Item(nome=nome,codigo=codigo, preco=preco, tipo_unidade=tipo_unidade, codigo_barras=codigo_barras)
        db.session.add(novo_item)
        db.session.commit()
        return redirect(url_for('listar_itens'))
    return render_template('novo_item.html')

@app.route('/itens/editar/<int:id>', methods=['GET', 'POST'])
def editar_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.preco = request.form['preco']
        item.codigo = request.form['codigo']
        item.tipo_unidade = request.form['tipo_unidade']
        item.codigo_barras = request.form['codigo_barras']
        db.session.commit()
        return redirect(url_for('listar_itens'))
    return render_template('editar_item.html', item=item)

@app.route('/itens/excluir/<int:id>', methods=['POST'])
def excluir_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('listar_itens'))

@app.route('/vendas/nova', methods=['POST', 'GET'])
def nova_venda():
    if 'carrinho' not in session:
        session['carrinho'] = []

    if request.method == 'POST':
        # Capture barcode input (assuming from a form field or other method)
        barcode = request.form.get('barcode')

        if barcode:
            # Extract item code from the barcode (assuming it's the first part)
            codigo_produto = barcode[:7]

            # Query the database for the product using the extracted code
            produto = Item.query.filter_by(codigo=codigo_produto).first()

            if produto:
                # Product found, proceed with adding to cart
                item_venda = {
                    'codigo_barras': produto.codigo,
                    'nome': produto.nome,
                    'quantidade': request.form.get('quantidade', type=float),
                    'preco_unitario': produto.preco,
                    'subtotal': produto.preco * request.form.get('quantidade', type=float)
                }
                session['carrinho'].append(item_venda)
                session.modified = True
            else:
                # Product not found, display error message
                return {'Produto não encontrado', 'erro'}, 404

        else:
            # Handle case where no barcode was provided
            return {'Campo código de barras obrigatório', 'erro'}, 400  # You can adjust the error code and message

    carrinho = session.get('carrinho', [])
    total_venda = sum(item['subtotal'] for item in carrinho)
    return render_template('nova_venda.html', carrinho=carrinho, total_venda=total_venda)

with app.app_context():
    if __name__ == '__main__':
        db.create_all()
        app.run(debug=True)
