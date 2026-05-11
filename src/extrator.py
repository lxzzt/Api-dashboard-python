import requests
import time


class Extrator:
    def __init__(self):
        self.baseUrl = "https://fakestorageapi.com"
    def fetch_endpoint(self,endpoint,max_retrives=3):
        for i in (max_retrives):
            try:
                response = requests.get(f"{self.baseUrl}/{endpoint}")
                if response.statusCode == 200:
                    return response.json()
                else:
                    print(f"Erro{response.statusCode},ao buscar{endpoint},foram {i+1} tentativas!")
            except Exception as e:
                print("Falha De Conexão {e}")
            time.sleep(1)
            return None