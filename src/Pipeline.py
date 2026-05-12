from Extrator import Extrator
from Transformer import Transformer
from DatabaseManager import DatabaseManager

class Pipeline:
    """
    Orquestrador do fluxo ETL. 
    Coordena a execução entre Extrator, Transformer e Database.
    """
    def __init__(self):
        # Instanciando as classes que criamos anteriormente
        self.extrator = Extrator()
        self.transformer = Transformer()
        # Exemplo de credenciais (Trade-off: Usar variáveis de ambiente para segurança)
        self.db = DatabaseManager(user='root', password='sua_senha', host='localhost', database='coco_bambu_db')

    def run(self):
        """
        Executa o fluxo completo com tratamento de erros global.
        """
        try:
            print("--- [Iniciando Pipeline de Dados] ---")

            # 1. ETAPA: EXTRAÇÃO
            print("Extraindo dados da API...")
            raw_carts = self.extrator.fetch_endpoint("carts")
            
            if not raw_carts:
                raise Exception("Falha crítica: Não foi possível obter dados da API.")

            # 2. ETAPA: TRANSFORMAÇÃO
            print("Transformando e limpando dados...")
            df_raw = self.transformer.to_dataframe(raw_carts)
            df_clean = self.transformer.clean_carts_data(df_raw)
            df_final = self.transformer.validate_quality(df_clean)

            # 3. ETAPA: CARGA (LOAD)
            print("Carregando dados no MySQL...")
            self.db.save_dataframe(df_final, "vendas_delivery")

            print("--- [Pipeline Finalizado com Sucesso!] ---")

        except Exception as e:
            # Fundamento: Logs de erro para monitoramento
            print(f"!!! ERRO NO PIPELINE: {e}")

if __name__ == "__main__":
    # Ponto de entrada do script
    app = Pipeline()
    app.run()