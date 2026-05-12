📊 Dashboard de Inteligência de Vendas - Delivery (Coco Bambu Style)
Este projeto simula um ecossistema de dados para uma operação de delivery de alto volume, como o Coco Bambu. O objetivo é transformar dados brutos de uma API pública em um Dashboard Executivo para suporte à tomada de decisão.

🧠 A Visão do Arquiteto
O projeto foi construído seguindo o princípio de Responsabilidade Única (SRP). Cada parte do código tem uma missão clara:

Extractor: O "garimpeiro" que busca os dados brutos.

Transformer: O "artesão" que limpa e cruza informações.

DatabaseManager: O "guardião" que garante a persistência no MySQL.

Pipeline: apenas coordena a execução entre as partes 

App (Streamlit): A "vitrine" que traduz números em insights visuais.

🚧 Desafios Técnicos e Superações
Durante o desenvolvimento, identifiquei limitações na fonte de dados que poderiam comprometer a qualidade do dashboard. Abaixo, explico como contornei cada uma:

0. problema da API,não achei uma API que simula exatamente o contexto de restaurantes.a mais proxima que achei foi uma api que simula um e-comerce.então tive que usá-la.

1. Problema do "Dashboard Vazio" (Limitação da API)
Limitação: Por padrão, a API retornava apenas 10 a 20 registros, o que tornava os gráficos irrelevantes para uma análise de negócio.

Solução: Implementei um parâmetro de limit=50 dinâmico na URL de extração.

Motivo: Isso forçou a API a entregar o volume máximo de dados disponível, permitindo uma visualização de tendências mais robusta.

2. Dados Desconexos (Cruzamento de Informações)
Limitação: Os dados de vendas (Carts) vinham apenas com IDs, sem nomes de produtos ou preços.

Solução: Desenvolvi um método de Merge (JOIN) no Pandas que unifica Carts, Products e Users em uma única tabela mestre.

Motivo: Isso permitiu calcular o Faturamento Total e o Ticket Médio, transformando dados técnicos em métricas de negócio reais.

3. Instabilidade de Conexão
Limitação: APIs externas podem falhar momentaneamente.

Solução: Implementei uma lógica de Retries (tentativas) no Extrator com pausas (time.sleep) entre elas.

Motivo: Garante que o pipeline seja resiliente e não quebre por instabilidades temporárias de rede.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.13

Manipulação de Dados: Pandas

Interface: Streamlit

Banco de Dados: MySQL via SQLAlchemy

Ambiente: Virtualenv (.venv) para isolamento de dependências

🚀 Como Executar
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/Api-dashboard-python.git
Ative o ambiente virtual:

Bash
.\.venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requeriments.txt
Inicie o Dashboard:

Bash
streamlit run src/app.py