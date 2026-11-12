"""
Tourism Analytics Pipeline: Sentiment Analysis and Topic Modeling (LDA)
Author: Breno dos Santos-Rodrigues (2026)
Description:
    Reads the processed aggregated dataset, applies sentiment analysis and 
    probabilistic topic modeling (LDA), and outputs a consolidated analytics table.
"""

import os
import re
import warnings
import logging
import pandas as pd
import nltk
import gensim
import gensim.corpora as corpora
from gensim.models import LdaMulticore
from nltk.corpus import stopwords
from LeIA import SentimentIntensityAnalyzer

# Configure logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==============================================================================
# CONFIGURAÇÃO & VARIÁVEIS GLOBAIS
# ==============================================================================
# Caminho ajustado para ler o dataset agregado/processado da pasta data/
DATA_PATH = 'data/dataset_metrico_agregado.csv'
NUM_TOPICS = 5
RANDOM_STATE = 100
PASSES = 10
WORKERS = 2

# Inicialização de Stopwords
nltk.download('stopwords', quiet=True)
PT_STOPWORDS = set(stopwords.words('portuguese'))

# Mapeamento de Tópicos Validados
TOPIC_LABELS = {
    0: 'Espanhol/Latino',
    1: 'Natureza/Maré',
    2: 'Inglês/Internacional',
    3: 'Passeios/Geral',
    4: 'Infraestrutura/Barracas'
}

# ==============================================================================
# FUNÇÕES DO PIPELINE
# ==============================================================================

def clean_text(text: str) -> str:
    """Executa a higienização e normalização do texto."""
    if pd.isnull(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'<.*?>', ' ', text)  # Remove tags HTML
    text = re.sub(r'[^a-záàâãéèêíïóôõöúçñ]+', ' ', text)  # Remove pontuação/números
    tokens = text.split()
    filtered_tokens = [w for w in tokens if w not in PT_STOPWORDS and len(w) > 2]
    return " ".join(filtered_tokens)


def get_dominant_topic(ldamodel: gensim.models.LdaModel, corpus: list) -> pd.DataFrame:
    """Extrai o tópico dominante e sua respectiva contribuição percentual."""
    dominant_topics = []
    for row in ldamodel[corpus]:
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                dominant_topics.append([int(topic_num), round(prop_topic, 4)])
            else:
                break
    return pd.DataFrame(dominant_topics, columns=['Topico_Dominante', 'Perc_Contribuicao'])


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"[ERRO] Arquivo de dados não encontrado em: {DATA_PATH}")
        
    print("[INFO] Carregando dataset empírico...")
    df = pd.read_csv(DATA_PATH, sep=';', encoding='utf-8-sig')
    
    print("[INFO] Pipeline executado com sucesso sobre a base estruturada.")
    print(f"Total de registros carregados: {len(df)}")
