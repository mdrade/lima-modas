# Li&Ma Modas — Loja Online

Loja online de roupas femininas e acessórios, com login, cadastro de usuários,
catálogo de produtos por categoria e carrinho de compras.

## Tecnologias

- **Backend:** Python + Flask
- **Banco de dados:** SQLite
- **Frontend:** HTML, CSS e JavaScript puro (sem frameworks)
- **Segurança:** senhas com hash (Werkzeug), sessão via cookie assinado,
  limite de tentativas de login (Flask-Limiter), variáveis sensíveis em `.env`

## Funcionalidades

- Cadastro e login de usuários (com sessão protegida por rota)
- Catálogo de produtos filtrável por categoria (Lançamentos, Vestidos,
  Conjuntos, Promoções)
- Carrossel de produtos em destaque
- Carrinho de compras persistente (localStorage), com controle de quantidade
- Layout responsivo com identidade visual própria

## Como rodar localmente

1. Clone o repositório e entre na pasta do projeto.
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Copie `.env.example` para `.env` e preencha a `SECRET_KEY`:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
5. Crie o banco de dados (cria um usuário de teste):
   ```
   python criar_banco.py
   ```
6. Rode o servidor:
   ```
   python app.py
   ```
7. Acesse `http://localhost:5000` no navegador.

## Estrutura do projeto

```
├── app.py
├── criar_banco.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   ├── tela.html
│   ├── cadastro.html
│   ├── loja.html
│   └── carrinho.html
└── static/
    ├── estilo.css / funcao.js / cadastro.js
    ├── loja.css / loja.js / carrinho.js
    └── (imagens de logo e produtos)
```

## Roadmap

- [ ] Integração com gateway de pagamento (cartão / Pix)
- [ ] Hospedagem em produção com HTTPS
- [ ] Painel administrativo para gerenciar produtos e pedidos

## Autor

Marcello Andrade Rodrigues dos Santos — [github.com/mdrade](https://github.com/mdrade)
