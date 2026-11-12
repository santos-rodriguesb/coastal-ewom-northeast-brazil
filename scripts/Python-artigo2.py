"""
UNIVERSIDADE FEDERAL DO PARANÁ (UFPR)
Programa de Pós-Graduação em Turismo (PPGTurismo)
Autor: Breno dos Santos-Rodrigues (2026)

Script de Replicabilidade - Artigo 2
Processamento de Linguagem Natural, Análise de Sentimentos (LeIA) e Modelagem de Tópicos (LDA)
"""

import os
import re
import warnings
import pandas as pd
import nltk
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaMulticore
from LeIA import SentimentIntensityAnalyzer
from pprint import pprint

# Silenciador de avisos de depreciação
warnings.filterwarnings("ignore", category=DeprecationWarning)
nltk.download('stopwords', quiet=True)
stops = set(stopwords.words('portuguese'))

def limpar_texto(texto):
    """Executa a higienização, remoção de ruídos e normalização do corpus textualmente."""
    if pd.isnull(texto): return ""
    texto = str(texto).lower()
    texto = re.sub(r'<.*?>', ' ', texto) # Remove tags HTML
    texto = re.sub(r'[^a-záàâãéèêíïóôõöúçñ]+', ' ', texto) # Remove pontuação e números
    palavras = texto.split()
    return " ".join([p for p in palavras if p not in stops and len(p) > 2])

def formatar_topicos_sentencas(ldamodel, corpus, textos):
    """Extrai o tópico dominante e sua respectiva contribuição percentual."""
    sent_topics_df = []
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                sent_topics_df.append([int(topic_num), round(prop_topic, 4)])
            else:
                break
    return pd.DataFrame(sent_topics_df, columns=['Topico_Dominante', 'Perc_Contribuicao'])

def main():
    # Caminho configurável conforme o seu ambiente
    caminho_entrada = "dados_nordeste_processado.xlsx"
    caminho_saida = "data/Resultado_Dissertacao_Final.csv"
    
    print("🚀 Iniciando o processamento do corpus...")
    df = pd.read_csv(caminho_entrada, sep=';', encoding='utf-8-sig')
    
    # 1. Limpeza
    df['texto_limpo'] = df['review_text'].apply(limpar_texto)
    
    # 2. Sentimentos (LeIA)
    analisador = SentimentIntensityAnalyzer()
    df['nota_sentimento'] = df['review_text'].apply(lambda t: analisador.polarity_scores(str(t))['compound'] if pd.notnull(t) else 0)
    df['sentimento'] = df['nota_sentimento'].apply(lambda n: 'Positivo' if n >= 0.05 else ('Negativo' if n <= -0.05 else 'Neutro'))
    
    # 3. Modelagem LDA
    dados_palavras = [str(frase).split() for frase in df['texto_limpo']]
    id2word = corpora.Dictionary(dados_palavras)
    id2word.filter_extremes(no_below=10, no_above=0.5)
    corpus = [id2word.doc2bow(text) for text in dados_palavras]
    
    lda_model = LdaMulticore(corpus=corpus, id2word=id2word, num_topics=5, random_state=100, passes=10, workers=2)
    
    # 4. Consolidação
    df_topicos = formatar_topicos_sentencas(lda_model, corpus, df['review_text'])
    df_final = pd.concat([df.reset_index(drop=True), df_topicos], axis=1)
    
    mapa_topicos = {0: 'Espanhol/Latino', 1: 'Natureza/Maré', 2: 'Inglês/Internacional', 3: 'Passeios/Geral', 4: 'Infraestrutura/Barracas'}
    df_final['Nome_Topico'] = df_final['Topico_Dominante'].map(mapa_topicos)
    
    df_final.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    print("✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
