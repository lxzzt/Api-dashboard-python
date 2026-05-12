import mysql.connector
from sqlalchemy import create_engine

class DatabaseManager:
    """
    Responsável pela conexão e persistência de dados no MySQL.
    Utiliza SQLAlchemy para facilitar a integração com DataFrames do Pandas.
    """

    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        # Trade-off: SQLAlchemy é mais lento que o conector puro, 
        # mas a integração com Pandas é nativa e muito mais segura.
        self.engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

    def save_dataframe(self, df, table_name):
        """
        Salva o DataFrame no banco de dados.
        """
        try:
            # if_exists='append': Mantém o histórico (essencial para métricas de negócio)
            # index=False: Não cria uma coluna extra para o índice do Pandas
            df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False)
            print(f"Sucesso: {len(df)} linhas inseridas na tabela {table_name}.")
        except Exception as e:
            print(f"Erro ao salvar no banco de dados: {e}")

    def execute_query(self, query):
        """
        Executa comandos SQL manuais (como criar tabelas ou limpar dados).
        """
        with self.engine.connect() as connection:
            return connection.execute(query)