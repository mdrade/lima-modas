function getCarrinho() {
  const dados = localStorage.getItem('carrinho');
  return dados ? JSON.parse(dados) : [];
}

function salvarCarrinho(itens) {
  localStorage.setItem('carrinho', JSON.stringify(itens));
}

function formatarPreco(valor) {
  return 'R$ ' + valor.toFixed(2).replace('.', ',');
}

function atualizarContadorCarrinho() {
  const itens = getCarrinho();
  const contador = document.getElementById('cartCount');
  if (contador) {
    contador.textContent = itens.reduce((soma, item) => soma + item.quantidade, 0);
  }
}

function renderizarCarrinho() {
  const itens = getCarrinho();
  const containerItens = document.getElementById('cartItems');
  const containerVazio = document.getElementById('cartEmpty');
  const containerResumo = document.getElementById('cartSummary');

  if (itens.length === 0) {
    containerItens.innerHTML = '';
    containerVazio.style.display = 'flex';
    containerResumo.style.display = 'none';
    return;
  }

  containerVazio.style.display = 'none';
  containerResumo.style.display = 'block';

  containerItens.innerHTML = itens.map((item, index) => `
    <div class="cart-item">
      <img src="/static/${item.imagem}" alt="${item.nome}">
      <div class="cart-item-info">
        <h4>${item.nome}</h4>
        <p>${formatarPreco(item.preco)}</p>
      </div>
      <div class="cart-item-qty">
        <button onclick="alterarQuantidade(${index}, -1)">−</button>
        <span>${item.quantidade}</span>
        <button onclick="alterarQuantidade(${index}, 1)">+</button>
      </div>
      <button class="cart-item-remove" onclick="removerItem(${index})" aria-label="Remover item">
        <i class="fa-solid fa-trash"></i>
      </button>
    </div>
  `).join('');

  const total = itens.reduce((soma, item) => soma + item.preco * item.quantidade, 0);
  document.getElementById('cartTotal').textContent = formatarPreco(total);
}

function alterarQuantidade(index, delta) {
  const itens = getCarrinho();
  itens[index].quantidade += delta;
  if (itens[index].quantidade <= 0) {
    itens.splice(index, 1);
  }
  salvarCarrinho(itens);
  renderizarCarrinho();
  atualizarContadorCarrinho();
}

function removerItem(index) {
  const itens = getCarrinho();
  itens.splice(index, 1);
  salvarCarrinho(itens);
  renderizarCarrinho();
  atualizarContadorCarrinho();
}

document.addEventListener('DOMContentLoaded', () => {
  renderizarCarrinho();
  atualizarContadorCarrinho();

  const btnFinalizar = document.getElementById('btnFinalizar');
  if (btnFinalizar) {
    btnFinalizar.addEventListener('click', () => {
      alert('Pedido realizado com sucesso! (simulação — ainda não envia pra nenhum backend)');
      localStorage.removeItem('carrinho');
      renderizarCarrinho();
      atualizarContadorCarrinho();
    });
  }
});