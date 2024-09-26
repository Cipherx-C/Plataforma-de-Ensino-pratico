from flask import Flask, render_template, request, redirect, url_for
from models import db, Voluntario, Projeto
from collections import Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skilllabs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Rota principal para a página de cadastro
@app.route('/')
def index():
    voluntarios = Voluntario.query.all()
    projetos = Projeto.query.all()
    
    # Contar quantos projetos estão em cada status
    status_count = Counter([projeto.status for projeto in projetos])
    projetos_status = [status_count.get('Pausado', 0), status_count.get('Em execução', 0), status_count.get('Pronto', 0)]
    return render_template('index.html', voluntarios=voluntarios, projetos=projetos, projetos_status=projetos_status)

# Rota para exibir o dashboard
@app.route('/dashboard')
def dashboard():
    voluntarios = Voluntario.query.all()
    projetos = Projeto.query.all()
    
    # Contar quantos projetos estão em cada status
    status_count = Counter([projeto.status for projeto in projetos])
    projetos_status = [status_count.get('Pausado', 0), status_count.get('Em execução', 0), status_count.get('Pronto', 0)]

    return render_template('dashboard.html', voluntarios=voluntarios, projetos=projetos, projetos_status=projetos_status)

# Rota para adicionar novos voluntários
@app.route('/add_voluntario', methods=['POST'])
def add_voluntario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    novo_voluntario = Voluntario(nome=nome, email=email)
    db.session.add(novo_voluntario)
    db.session.commit()
    return redirect(url_for('index'))

# Rota para adicionar novos projetos
@app.route('/add_projeto', methods=['POST'])
def add_projeto():
    titulo = request.form.get('titulo')
    status = request.form.get('status')
    novo_projeto = Projeto(titulo=titulo, status=status)
    db.session.add(novo_projeto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/projetos_voluntarios')
def projetos_voluntarios():
    voluntarios = Voluntario.query.all()
    projetos = Projeto.query.all()
    
    return render_template('projetos_voluntarios.html', voluntarios=voluntarios, projetos=projetos)

@app.route('/delete_projeto/<int:id>', methods=['POST'])
def delete_projeto(id):
    projeto = Projeto.query.get(id)
    if projeto:
        db.session.delete(projeto)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_voluntario/<int:id>', methods=['POST'])
def delete_voluntario(id):
    voluntario = Voluntario.query.get(id)
    if voluntario:
        db.session.delete(voluntario)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_voluntario_projeto/<int:projeto_id>', methods=['POST'])
def add_voluntario_projeto(projeto_id):
    voluntario_ids = request.form.getlist('voluntarios')  # Obtém a lista de IDs de voluntários selecionados
    projeto = Projeto.query.get(projeto_id)

    if projeto:
        for voluntario_id in voluntario_ids:
            voluntario = Voluntario.query.get(voluntario_id)
            if voluntario:
                projeto.voluntarios.append(voluntario)  # Adiciona o voluntário ao projeto

        db.session.commit()
    return redirect(url_for('projetos_voluntarios'))  # Redireciona para a página de projetos



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    app.run(debug=True)
