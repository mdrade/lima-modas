// ---------- Carrinho (salvo no localStorage, funciona em qualquer página do site) ----------
function getCarrinho() {
  const dados = localStorage.getItem('carrinho');
  return dados ? JSON.parse(dados) : [];
}

function salvarCarrinho(itens) {
  localStorage.setItem('carrinho', JSON.stringify(itens));
}

function atualizarContadorCarrinho() {
  const itens = getCarrinho();
  const contador = document.getElementById('cartCount');
  if (contador) {
    contador.textContent = itens.reduce((soma, item) => soma + item.quantidade, 0);
  }
}

function addToCart(nome, preco, imagem) {
  const itens = getCarrinho();
  const existente = itens.find(item => item.nome === nome);

  if (existente) {
    existente.quantidade += 1;
  } else {
    itens.push({ nome, preco, imagem, quantidade: 1 });
  }

  salvarCarrinho(itens);
  atualizarContadorCarrinho();
  alert(`"${nome}" foi adicionado ao seu carrinho!`);
}

document.addEventListener('DOMContentLoaded', atualizarContadorCarrinho);

// ---------- Carrossel de produtos no topo da loja ----------
const slides = document.querySelectorAll('.carousel-slide');
const dots = document.querySelectorAll('.dot');
let currentSlide = 0;
let carouselTimer = null;

function showSlide(index) {
  slides[currentSlide].classList.remove('active');
  dots[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
}

function nextSlide() {
  showSlide(currentSlide + 1);
}

function prevSlide() {
  showSlide(currentSlide - 1);
}

function goToSlide(index) {
  showSlide(index);
  resetAutoplay();
}

function startAutoplay() {
  carouselTimer = setInterval(nextSlide, 5000);
}

function resetAutoplay() {
  clearInterval(carouselTimer);
  startAutoplay();
}

if (slides.length > 0) {
  startAutoplay();

  const carousel = document.querySelector('.hero-carousel');
  carousel.addEventListener('mouseenter', () => clearInterval(carouselTimer));
  carousel.addEventListener('mouseleave', startAutoplay);
}