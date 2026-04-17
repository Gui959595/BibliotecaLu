from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Livro
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    return response


# HOME
@app.route("/")
def index():
    livros = Livro.query.all()
    return render_template("index.html", Livros=livros)


# FORM (CRIAR + EDITAR)
@app.route("/form", methods=["GET", "POST"])
def form():
    id = request.args.get("id")
    livro = Livro.query.get(id) if id else None

    if request.method == "GET":
        return render_template("form.html", livro=livro)

    # POST
    nome = request.form.get("nome")
    autor = request.form.get("autor")
    ano_publicacao = request.form.get("ano")
    editora = request.form.get("editora")
    genero = request.form.get("genero")
    isbn = request.form.get("isbn")

    # 🔴 VALIDAÇÃO CAMPOS OBRIGATÓRIOS
    if not nome or not autor:
        return render_template(
            "form.html",
            livro=livro,
            erro="Nome e Autor são obrigatórios!"
        )

    if not isbn:
        isbn = None

    try:
        # EDITAR
        if livro:
            # 🔴 valida ISBN duplicado (exceto o próprio livro)
            if isbn:
                existente = Livro.query.filter_by(isbn=isbn).first()
                if existente and existente.id != livro.id:
                    return render_template(
                        "form.html",
                        livro=livro,
                        erro="ISBN já existe!"
                    )

            livro.nome = nome
            livro.autor = autor
            livro.ano_publicacao = ano_publicacao
            livro.editora = editora
            livro.genero = genero
            livro.isbn = isbn

        # CRIAR
        else:
            if isbn:
                existente = Livro.query.filter_by(isbn=isbn).first()
                if existente:
                    return render_template(
                        "form.html",
                        erro="ISBN já existe!"
                    )

            novo = Livro(
                nome=nome,
                autor=autor,
                ano_publicacao=ano_publicacao,
                editora=editora,
                genero=genero,
                isbn=isbn
            )
            db.session.add(novo)

        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return render_template("form.html", livro=livro, erro="Erro ao salvar!")

    return redirect(url_for("index"))


# DELETAR
@app.route('/deletar/<int:id>', methods=["POST"])
def deletar(id):
    livro = Livro.query.get(id)

    if livro:
        db.session.delete(livro)
        db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)