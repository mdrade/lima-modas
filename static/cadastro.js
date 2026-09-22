document.getElementById('cadastroForm').addEventListener('submit', function (event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const senha = document.getElementById('password').value;
  const confirmarSenha = document.getElementById('confirmarSenha').value;

  if (senha !== confirmarSenha) {
    alert('As senhas não coincidem.');
    return;
  }

  fetch('/api/cadastro', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, senha })
  })
    .then(response => response.json())
    .then(data => {
      if (data.sucesso) {
        alert('Cadastro realizado com sucesso! Agora você já pode entrar.');
        window.location.href = '/';
      } else {
        alert(data.mensagem || 'Não foi possível concluir o cadastro.');
      }
    })
    .catch(error => {
      console.error('Erro ao conectar com o servidor:', error);
      alert('Erro ao conectar com o servidor.');
    });
});