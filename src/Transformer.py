import pandas as pd

class Transformer:
    """
    Responsável pela limpeza, transformação e garantia de qualidade (Data Quality)
    dos dados brutos extraídos da API.
    """
    
    def __init__(self):
        pass

    def to_dataframe(self, raw_data):
        """Converte JSON bruto em DataFrame, tratando casos de dados vazios."""
        if not raw_data:
            print("Aviso: Dados brutos vazios recebidos.")
            return pd.DataFrame()
        return pd.DataFrame(raw_data)

    def clean_carts_data(self, df_carts):
        """
        Aplica regras de negócio e limpeza para os dados de carrinhos (Carts).
        """
        if df_carts.empty:
            return df_carts

        # 1. Conversão de tipos (Fundamento: Garantir que datas sejam tratáveis)
        df_carts['date'] = pd.to_datetime(df_carts['date'])

        # 2. Explodir a coluna 'products' (Trade-off: Normalização para análise detalhada)
        # Como um carrinho tem vários produtos, 'explodimos' a lista para ter uma linha por produto.
        df_normalized = df_carts.explode('products').reset_index(drop=True)
        
        # 3. Extrair dados da coluna 'products' que agora é um dicionário
        # Criamos colunas separadas para productId e quantity
        df_normalized['productId'] = df_normalized['products'].apply(lambda x: x['productId'] if isinstance(x, dict) else None)
        df_normalized['quantity'] = df_normalized['products'].apply(lambda x: x['quantity'] if isinstance(x, dict) else None)
        
        # Removemos a coluna original complexa
        df_normalized = df_normalized.drop(columns=['products'])

        return df_normalized

    def validate_quality(self, df):
        """
        Data Quality: Filtra registros que podem sujar os relatórios do Coco Bambu.
        """
        # Exemplo de Trade-off: Remover linhas com quantidades nulas ou negativas
        initial_count = len(df)
        df = df[df['quantity'] > 0].copy()
        
        dropped = initial_count - len(df)
        if dropped > 0:
            print(f"Data Quality: {dropped} registros inconsistentes removidos.")
            
        return df
    def merge_data(self, df_carts, df_products, df_users):
        """Cruza carrinhos com produtos para saber o preço e usuários para saber o nome."""
        
        # 1. Primeiro, limpamos os carrinhos (usando o método que você já tem)
        df_flat_carts = self.clean_carts_data(df_carts)
        
        # 2. Cruzamos com Produtos para ter o 'price' e 'category'
        # Fazemos um merge (igual ao JOIN do SQL) usando o productId
        df_merged = pd.merge(df_flat_carts, df_products[['id', 'price', 'category', 'title']], 
                            left_on='productId', right_on='id', how='left')
        
        # 3. Cruzamos com Usuários para ter o 'username' e 'city'
        df_final = pd.merge(df_merged, df_users[['id', 'username', 'address']], 
                            left_on='userId', right_on='id', how='left')
        
        # 4. Cálculo de Negócio: Faturamento por item
        df_final['total_price'] = df_final['quantity'] * df_final['price']
        
        return df_final