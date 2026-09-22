document.getElementById('loginForm').addEventListener('submit', function (event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const senha = document.getElementById('password').value;

  fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, senha })
  })
    .then(response => response.json())
    .then(data => {
      if (data.sucesso) {
        window.location.href = '/loja';
      } else {
        alert(data.mensagem || 'E-mail ou senha incorretos.');
      }
    })
    .catch(error => {
      console.error('Erro ao conectar com o servidor:', error);
      alert('Erro ao conectar com o servidor.');
    });
});