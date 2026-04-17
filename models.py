from db import db

class Livro(db.Model):

    id =                db.Column(db.Integer, primary_key=True)
    nome =              db.Column(db.String(100), nullable=False)
    autor =             db.Column(db.String(100), nullable=False)
    ano_publicacao =    db.Column(db.Integer, nullable=True)
    editora =           db.Column(db.String(100), nullable=True)
    genero =            db.Column(db.String(50), nullable=True)
    isbn =              db.Column(db.String(13), unique=True, nullable=True)
    
    def __repr__(self):
        return f"Livro: ('{self.nome}', '{self.autor}', '{self.ano_publicacao}', '{self.editora}', '{self.genero}', '{self.isbn}')" 