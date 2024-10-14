#importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta
# criar as funções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao


lista_acoes = ["ITUB4.SA", "BITCOIN", "PETR4.SA", "VALE3.SA", "DÓLAR"]
#preparar visualizacoes
st.sidebar.header("Filtros")
dados = carregar_dados(lista_acoes)

#filtros de accoes
lista_view = st.sidebar.multiselect("Escolha as ações para visualizar",dados.columns)
if lista_view:
    dados = dados[lista_view]
    if len(lista_view) == 1:
        accao_unica = lista_view[0]
        dados = dados.rename(columns = {accao_unica: "Close"})  
        

#filtros de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione periodo", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final), step=timedelta(days=30))
print(dados)
# Criar interface
st.write("""
         # App precos de ações
         o  gráfico abaixo representa a evolução de preços de acções
         """)

# Criar Grafico
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]
st.line_chart(dados)