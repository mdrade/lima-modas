import sqlite3
from werkzeug.security import generate_password_hash

# Conecta (ou cria, se ainda não existir) o arquivo do banco de dados
conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()

# Cria a tabela de usuários, se ainda não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
""")

# Cria um usuário de teste com a senha "hasheada"
# (nunca guarde senha em texto puro no banco!)
email_teste = "aluno@teste.com"
senha_teste = "python123"
senha_hash = generate_password_hash(senha_teste)

try:
    cursor.execute(
        "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
        (email_teste, senha_hash)
    )
    conexao.commit()
    print(f"Usuário de teste criado: {email_teste} / senha: {senha_teste}")
except sqlite3.IntegrityError:
    print("Esse usuário de teste já existe no banco.")

conexao.close()