# backend/train.py

import os
import json
import numpy as np
import pandas as pd

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split

# Importamos tu función de limpieza
from preprocess import load_and_clean

# 1) Carga y limpieza de datos
df = load_and_clean(path=r'C:\Users\ARMANDO GUERRA\Desktop\phishing-detector\data\phishing_email.csv')
texts = df['cleaned'].tolist()
labels = df['label'].astype(int).tolist()

# 2) Tokenización
MAX_NUM_WORDS = 10000
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(texts)

# Guardamos el tokenizer para la API luego
with open('backend/tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(tokenizer.to_json())

sequences = tokenizer.texts_to_sequences(texts)

# 3) Padding
MAX_SEQUENCE_LENGTH = 200
X = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
y = np.array(labels)

# 4) División train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# 5) Definición del modelo LSTM
EMBEDDING_DIM = 128

model = Sequential([
    Embedding(input_dim=MAX_NUM_WORDS, output_dim=EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH),
    LSTM(64),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()

# 6) Callbacks
os.makedirs('backend/models', exist_ok=True)

checkpoint = ModelCheckpoint(
    'backend/models/mejor_modelo.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
early_stop = EarlyStopping(
    monitor='val_accuracy',
    patience=3,
    restore_best_weights=True,
    verbose=1
)

# 7) Entrenamiento
history = model.fit(
    X_train, y_train,
    validation_split=0.1,
    epochs=10,
    batch_size=64,
    callbacks=[checkpoint, early_stop],
    verbose=2
)

# 8) Evaluación
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f'\nPrecisión en test: {acc:.4f} — Pérdida en test: {loss:.4f}')

# 9) Guardar el mejor modelo final
model.save('backend/models/modelo_phishing.h5')
print('\nModelo final guardado en backend/models/modelo_phishing.h5')

