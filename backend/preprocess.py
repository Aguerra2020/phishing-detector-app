# backend/preprocess.py

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Descarga de stopwords de NLTK (solo la primera vez)
nltk.download('stopwords')

# Conjunto de palabras vacías en inglés
STOPWORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """
    Limpia un texto de correo:
    - Pasa a minúsculas.
    - Elimina etiquetas HTML.
    - Elimina URLs.
    - Quita caracteres no alfanuméricos.
    - Elimina stopwords.
    """
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)                    # quitar HTML
    text = re.sub(r'http\S+|www\.\S+', ' ', text)           # quitar URLs
    text = re.sub(r'[^a-z0-9\s]', ' ', text)                # quitar puntuación
    words = [w for w in text.split() if w not in STOPWORDS]
    return ' '.join(words)

def load_and_clean(path: str = 'C:/Users/ARMANDO GUERRA/Desktop/phishing-detector/data/phishing_email.csv') -> pd.DataFrame:
    """
    Carga un CSV con columnas 'text_combined' y 'label', renombra la columna
    de texto a 'text', limpia el texto y devuelve un DataFrame con columnas
    ['cleaned', 'label'].
    """
    # 1. Cargar el CSV
    df = pd.read_csv(path)

    # 2. Renombrar text_combined → text si existe
    if 'text_combined' in df.columns:
        df = df.rename(columns={'text_combined': 'text'})

    # 3. Eliminar filas con texto o etiqueta faltante
    df = df.dropna(subset=['text', 'label'])

    # 4. Limpiar el texto
    df['cleaned'] = df['text'].astype(str).apply(clean_text)

    # 5. Devolver solo texto limpio y etiqueta
    return df[['cleaned', 'label']]

if __name__ == '__main__':
    df = load_and_clean()
    print(df.head(5))
    print(f"Total registros procesados: {len(df)}")
    print("Distribución de etiquetas:")
    print(df['label'].value_counts())
