const inputGrid = document.getElementById('input-grid');
const resultado = document.getElementById('resultado');

// Cria 60 campos de input
for (let i = 0; i < 60; i++) {
  const input = document.createElement('input');
  input.type = 'number';
  input.step = 'any';
  input.placeholder = `#${i + 1}`;
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === 'Tab') {
      event.preventDefault();
      const nextInput = inputGrid.children[i + 1];
      if (nextInput) nextInput.focus();
    }
  });
  inputGrid.appendChild(input);
}

document.getElementById('prever-btn').addEventListener('click', async () => {
  const inputs = document.querySelectorAll('#input-grid input');
  const prices = Array.from(inputs).map(input => parseFloat(input.value));

  if (prices.some(isNaN)) {
    alert('Preencha todos os campos com valores numéricos.');
    return;
  }

  if (prices.length !== 60) {
    alert('Você deve fornecer exatamente 60 valores.');
    return;
  }

  resultado.textContent = 'Calculando previsão...';

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prices })
    });

    const data = await response.json();
    if (response.ok) {
      resultado.textContent = `📈 Previsão do próximo preço: R$ ${data.previsao}`;
    } else {
      resultado.textContent = `Erro: ${data.detail}`;
    }
  } catch (error) {
    resultado.textContent = `Erro na requisição: ${error.message}`;
  }
});
