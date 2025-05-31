// frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
  const checkBtn = document.getElementById('checkBtn');
  const emailText = document.getElementById('emailText');
  const resultDiv = document.getElementById('result');
  const resultIcon = document.getElementById('resultIcon');
  const resultText = document.getElementById('resultText');

  checkBtn.addEventListener('click', () => {
    const text = emailText.value.trim();
    if (!text) {
      alert('Por favor, ingresa el contenido del correo.');
      return;
    }

    // Mostrar indicador de carga y ocultar resultado previo
    checkBtn.disabled = true;
    checkBtn.textContent = 'Verificando...';
    resultDiv.classList.add('hidden');
    resultDiv.classList.remove('phishing', 'legit', 'show');

    // Realiza petición POST a la API
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: text })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`Error en la petición: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Restaurar botón
        checkBtn.disabled = false;
        checkBtn.textContent = 'Verificar';

        // Mostrar resultado
        if (data.prediction === 'phishing') {
          resultDiv.classList.add('phishing');
          resultIcon.textContent = '⚠️';
          resultText.textContent = `Phishing detectado (Probabilidad: ${(
            data.probability * 100
          ).toFixed(2)}%)`;
        } else {
          resultDiv.classList.add('legit');
          resultIcon.textContent = '✔️';
          resultText.textContent = `Correo legítimo (Confianza: ${(
            (1 - data.probability) * 100
          ).toFixed(2)}%)`;
        }
        resultDiv.classList.remove('hidden');
        // Añadir animación de aparición
        setTimeout(() => resultDiv.classList.add('show'), 10);
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al conectar con el servidor.');
        checkBtn.disabled = false;
        checkBtn.textContent = 'Verificar';
      });
  });
});
