from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo para os Voluntários
class Voluntario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    projetos = db.relationship('Projeto', secondary='voluntario_projeto', backref='voluntarios')

# Modelo para os Projetos
class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Pausado, Em execução, Pronto

# Tabela associativa
voluntario_projeto = db.Table('voluntario_projeto',
    db.Column('voluntario_id', db.Integer, db.ForeignKey('voluntario.id')),
    db.Column('projeto_id', db.Integer, db.ForeignKey('projeto.id'))
)
