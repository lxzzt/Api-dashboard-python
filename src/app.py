import streamlit as st
import pandas as pd
from Extrator import Extrator
from Transformer import Transformer
from DatabaseManager import DatabaseManager

# Configuração da página do Dashboard
st.set_page_config(page_title="Coco Bambu - Data Intelligence", layout="wide")

st.title("📊 Dashboard de Inteligência de Vendas")
st.sidebar.header("Configurações do Pipeline")

# Instanciando as classes (Fundamentos: Reuso de lógica)
extrator = Extrator()
transformer = Transformer()

def run_etl_process():
    """Executa o pipeline e retorna os dados para o dashboard"""
    with st.spinner('Extraindo e transformando dados...Clientes,Pedidos e Carrinhos'):
        raw_carts = extrator.fetch_endpoint("carts")
        raw_products = extrator.fetch_endpoint("products")
        raw_users = extrator.fetch_endpoint("users")
        if raw_carts and raw_products and raw_users:
            df_carts = transformer.to_dataframe(raw_carts)
            df_products = transformer.to_dataframe(raw_products)
            df_users = transformer.to_dataframe(raw_users)
            
            # O GRANDE MERGE
            df_final = transformer.merge_data(df_carts, df_products, df_users)
            return df_final
    return None

# Botão para disparar o Pipeline
if st.sidebar.button('Executar Pipeline ETL'):
    data = run_etl_process()
    if data is not None:
        st.success("Pipeline Concluído!")
        
        # Novas Métricas de Negócio
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Total", f"R$ {data['total_price'].sum():.2f}")
        c2.metric("Ticket Médio", f"R$ {data['total_price'].mean():.2f}")
        c3.metric("Total de Itens", int(data['quantity'].sum()))

        # Gráfico de Faturamento por Categoria (Muito útil para restaurante!)
        st.subheader("Faturamento por Categoria de Produto")
        chart_data = data.groupby('category')['total_price'].sum()
        st.bar_chart(chart_data)
        
        st.subheader("Dados Consolidados")
        st.write(data[['date', 'username', 'title', 'quantity', 'total_price']])
    else:
        st.error("Erro ao processar dados. Verifique os logs.")

else:
    st.info("Clique no botão lateral para iniciar a extração de dados.")