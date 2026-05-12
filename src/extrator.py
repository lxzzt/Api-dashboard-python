import requests
import time
class Extrator:
    def __init__(self):
        self.base_url = "https://fakestoreapi.com"
    def fetch_endpoint(self,endpoint,max_retrives=3,limit=50):
        url = f"{self.base_url}/{endpoint}?limit={limit}"
        for i in range(max_retrives):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Erro{response.status_code},ao buscar{endpoint},foram {i+1} tentativas!")

            except Exception as e:
                print(f"Falha De Conexão {e}")

            time.sleep(1)
        return None