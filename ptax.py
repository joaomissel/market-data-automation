import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# DATA ATUAL - SÃO PAULO
# =========================

agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

data = agora.strftime("%Y-%m-%d")

print(
    "Data de São Paulo:",
    agora.strftime("%Y-%m-%d %H:%M:%S %Z")
)


# =========================
# API PTAX - BANCO CENTRAL
# =========================

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    f"CotacaoDolarDia(dataCotacao=@dataCotacao)?"
    f"@dataCotacao='{agora.strftime('%m-%d-%Y')}'"
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
# TRATAMENTO DOS DADOS
# =========================

dados = response.json()

cotacoes = dados["value"]

if len(cotacoes) == 0:

    print("Nenhuma cotação encontrada para a data.")

else:

    cotacao = cotacoes[0]

    resultado = [{
        "Data": data,
        "PTAX Compra": cotacao["cotacaoCompra"],
        "PTAX Venda": cotacao["cotacaoVenda"],
        "Data/Hora Cotação": cotacao["dataHoraCotacao"]
    }]

    df = pd.DataFrame(resultado)


    # =========================
    # RESULTADO
    # =========================

    print("\n==============================")
    print("PTAX")
    print("==============================\n")

    print(df.to_string(index=False))


    # =========================
    # EXPORTAR CSV
    # =========================

    df.to_csv(
        "ptax.csv",
        index=False
    )

    print("\nArquivo ptax.csv criado com sucesso.")
