import streamlit as st
import pandas as pd
from src.Extrator import Extractor
from src.Transformer import Transformer
from src.DatabaseManager import DatabaseManager

# Configuração da página do Dashboard
st.set_page_config(page_title="Coco Bambu - Data Intelligence", layout="wide")

st.title("📊 Dashboard de Inteligência de Vendas")
st.sidebar.header("Configurações do Pipeline")

# Instanciando as classes (Fundamentos: Reuso de lógica)
extractor = Extractor()
transformer = Transformer()

def run_etl_process():
    """Executa o pipeline e retorna os dados para o dashboard"""
    with st.spinner('Extraindo e transformando dados...'):
        raw_carts = extractor.fetch_endpoint("carts")
        if raw_carts:
            df_raw = transformer.to_dataframe(raw_carts)
            df_clean = transformer.clean_carts_data(df_raw)
            return transformer.validate_quality(df_clean)
    return None

# Botão para disparar o Pipeline
if st.sidebar.button('Executar Pipeline ETL'):
    data = run_etl_process()
    if data is not None:
        st.success("Dados processados com sucesso!")
        
        # Exibindo métricas básicas (Métricas de Negócio solicitadas na vaga)
        col1, col2 = st.columns(2)
        col1.metric("Total de Pedidos", len(data))
        col2.metric("Qtd. Itens Processados", data['quantity'].sum())

        # Visualização de Dados
        st.subheader("Visualização dos Dados Transformados")
        st.dataframe(data) # Tabela interativa

        # Gráfico simples de exemplo
        st.subheader("Distribuição de Quantidade por Pedido")
        st.bar_chart(data.set_index('date')['quantity'])
    else:
        st.error("Erro ao processar dados. Verifique os logs.")

else:
    st.info("Clique no botão lateral para iniciar a extração de dados.")