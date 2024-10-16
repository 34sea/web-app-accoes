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

@st.cache_data
def carrgar_tickers_accoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers
#lista_acoes = ["ITUB4.SA", "BITCOIN", "PETR4.SA", "VALE3.SA", "DÓLAR"]
lista_acoes = carrgar_tickers_accoes()
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

texto_performance_ativos = " "

if len(lista_view) == 0:
    lista_view = list(dados.column)
    
for acao in lista_view:
    performance_ativo  = dados[acao].iloc[-1] / dados[acao].iloc[0] -1
    performance_ativo = float(performance_ativo )
    texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"

st.write(f"""
         ### Performance dos ativos

         Essa foi a performance de cada ativo no periodo selecionado

         {texto_performance_ativos}
         """)
