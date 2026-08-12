import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# DATA ATUAL - BRASIL
# =========================

agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

data = agora.strftime("%m-%d-%Y")

print("Data de São Paulo:", agora.strftime("%Y-%m-%d"))


# =========================
# API PTAX - BANCO CENTRAL
# =========================

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    f"CotacaoDolarDia(dataCotacao=@dataCotacao)?"
    f"@dataCotacao='{data}'"
    "&$format=json"
)


# =========================
# CONSULTA
# =========================

response = requests.get(
    url,
    timeout=15
)

print("Status API:", response.status_code)


# =========================
# DADOS
# =========================

dados = response.json()

print("\nResposta da API:")
print(dados)
