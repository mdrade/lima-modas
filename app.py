import os
import re
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()  # lê as variáveis definidas no arquivo .env, se ele existir

app = Flask(__name__)

# A SECRET_KEY assina os cookies de sessão. Em produção ela SEMPRE tem que vir
# de uma variável de ambiente — nunca deixe uma chave real escrita no código.
app.secret_key = os.environ.get("SECRET_KEY")

# Cookies de sessão mais seguros
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# Só exige HTTPS quando USE_HTTPS=True no .env (ou seja, depois que o site
# já estiver publicado de verdade com HTTPS configurado)
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("USE_HTTPS", "False") == "True"

# Modo debug: desligado por padrão (mostrar erros detalhados em produção é um
# risco de segurança). Pra desenvolver no seu computador, defina
# FLASK_DEBUG=True no seu .env.
DEBUG_MODE = os.environ.get("FLASK_DEBUG", "False") == "True"

# Limita quantas tentativas de login/cadastro cada IP pode fazer por minuto,
# pra dificultar ataques de força bruta tentando adivinhar senha.
limiter = Limiter(key_func=get_remote_address, app=app, default_limits=[])

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# Catálogo de produtos. Cada produto pode pertencer a mais de uma categoria,
# por isso "categorias" é uma lista (ex: "lancamentos" + "vestidos" ao mesmo tempo).
PRODUTOS = [
    {
        "id": 1,
        "nome": "Conjunto Pink Elegance",
        "imagem": "conjunto-pink.jpg",
        "preco": 189.90,
        "preco_antigo": None,
        "tag": "Novo",
        "categorias": ["lancamentos", "conjuntos"],
    },
    {
        "id": 2,
        "nome": "Macacão Terracota",
        "imagem": "macacao-terracota.jpg",
        "preco": 219.90,
        "preco_antigo": None,
        "tag": None,
        "categorias": ["conjuntos"],
    },
    {
        "id": 3,
        "nome": "Blusa Animal Print One Shoulder",
        "imagem": "blusa-animal-print.jpg",
        "preco": 99.90,
        "preco_antigo": None,
        "tag": None,
        "categorias": ["lancamentos"],
    },
    {
        "id": 4,
        "nome": "Vestido Longo Animal Print",
        "imagem": "vestido-animal-print.jpg",
        "preco": 229.90,
        "preco_antigo": 279.90,
        "tag": "Oferta",
        "categorias": ["vestidos", "promocoes"],
    },
    {
        "id": 5,
        "nome": "Conjunto Preto & Verde",
        "imagem": "conjunto-preto-verde.jpg",
        "preco": 199.90,
        "preco_antigo": None,
        "tag": None,
        "categorias": ["conjuntos"],
    },
    {
        "id": 6,
        "nome": "Vestido Preto Detalhe Verde",
        "imagem": "vestido-preto-verde.jpg",
        "preco": 159.90,
        "preco_antigo": None,
        "tag": "Novo",
        "categorias": ["lancamentos", "vestidos"],
    },
    {
        "id": 7,
        "nome": "Camiseta Estampa Máscara Pena Verde",
        "imagem": "camiseta-pena-verde.jpg",
        "preco": 79.90,
        "preco_antigo": None,
        "tag": None,
        "categorias": ["promocoes"],
    },
    {
        "id": 8,
        "nome": "Camiseta Estampa Máscara Pena Azul",
        "imagem": "camiseta-pena-azul.jpg",
        "preco": 79.90,
        "preco_antigo": None,
        "tag": None,
        "categorias": ["promocoes"],
    },
]

# Nome de exibição de cada categoria, usado no título da página
NOMES_CATEGORIA = {
    "lancamentos": "Lançamentos",
    "vestidos": "Vestidos",
    "conjuntos": "Conjuntos",
    "promocoes": "Promoções",
}


@app.route("/")
def tela_login():
    return render_template("tela.html")


@app.route("/cadastro")
def tela_cadastro():
    return render_template("cadastro.html")


@app.route("/loja")
def loja():
    if "usuario_email" not in session:
        return redirect(url_for("tela_login"))

    categoria = request.args.get("categoria")

    if categoria and categoria in NOMES_CATEGORIA:
        produtos_filtrados = [p for p in PRODUTOS if categoria in p["categorias"]]
        titulo_secao = NOMES_CATEGORIA[categoria]
    else:
        categoria = None
        produtos_filtrados = PRODUTOS
        titulo_secao = "Destaques da Semana"

    return render_template(
        "loja.html",
        produtos=produtos_filtrados,
        todos_produtos=PRODUTOS,
        categoria_ativa=categoria,
        titulo_secao=titulo_secao,
    )


@app.route("/carrinho")
def carrinho():
    if "usuario_email" not in session:
        return redirect(url_for("tela_login"))
    return render_template("carrinho.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("tela_login"))


@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha e-mail e senha"}), 400

    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
    except sqlite3.Error:
        return jsonify({"sucesso": False, "mensagem": "Erro ao acessar o banco de dados"}), 500
    finally:
        conexao.close()

    if resultado and check_password_hash(resultado[0], senha):
        session.clear()
        session["usuario_email"] = email
        return jsonify({"sucesso": True})
    else:
        return jsonify({"sucesso": False, "mensagem": "E-mail ou senha incorretos"}), 401


@app.route("/api/cadastro", methods=["POST"])
@limiter.limit("5 per minute")
def cadastro():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha:
        return jsonify({"sucesso": False, "mensagem": "Preencha e-mail e senha"}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"sucesso": False, "mensagem": "Digite um e-mail válido"}), 400

    if len(senha) < 6:
        return jsonify({"sucesso": False, "mensagem": "A senha precisa ter pelo menos 6 caracteres"}), 400

    senha_hash = generate_password_hash(senha)

    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
            (email, senha_hash)
        )
        conexao.commit()
        return jsonify({"sucesso": True})
    except sqlite3.IntegrityError:
        return jsonify({"sucesso": False, "mensagem": "Esse e-mail já está cadastrado"}), 409
    except sqlite3.Error:
        return jsonify({"sucesso": False, "mensagem": "Erro ao acessar o banco de dados"}), 500
    finally:
        conexao.close()


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE)