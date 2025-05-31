# backend/app.py

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

from preprocess import clean_text

# 1) Inicializa Flask y habilita CORS (para que el frontend pueda hacer solicitudes)
app = Flask(__name__)
CORS(app)

# 2) Carga del modelo entrenado
MODEL_PATH = 'backend/models/mejor_modelo.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# 3) Carga del tokenizer (como string JSON para tokenizer_from_json)
with open('backend/tokenizer.json', 'r', encoding='utf-8') as f:
    token_json_str = f.read()
tokenizer = tokenizer_from_json(token_json_str)

# 4) Parámetros de secuencia
MAX_SEQUENCE_LENGTH = 200

# 5) Endpoint /predict para recibir el texto y devolver la predicción
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    text = data.get('text', '')

    # a) Limpieza del texto usando la misma función de preprocess.py
    cleaned = clean_text(text)

    # b) Tokenización y padding a la longitud fija
    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)

    # c) Predicción con el modelo
    prob = model.predict(padded)[0][0]
    label = 'phishing' if prob > 0.5 else 'legit'

    # d) Respuesta en formato JSON
    return jsonify({
        'prediction': label,
        'probability': float(prob)
    })

if __name__ == '__main__':
    app.run(debug=True)
