#importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
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

dados = carregar_dados(lista_acoes)

lista_view = st.multiselect("Escolha as ações para visualizar",dados.columns)
if lista_view:
    dados = dados[lista_view]
    if len(lista_view) == 1:
        accao_unica = lista_view[0]
        dados = dados.rename(columns = {accao_unica: "Close"})  
        

print(dados)
# Criar interface
st.write("""
         # App precos de ações
         o  gráfico abaixo representa a evolução de preços de acções
         """)

# Criar Grafico

st.line_chart(dados)