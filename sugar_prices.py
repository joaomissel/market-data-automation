import requests
import json
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# CONFIGURAÇÕES
# =========================

headers = {
    "User-Agent": "Mozilla/5.0"
}


# =========================
# HORÁRIO DE NEW YORK
# =========================

agora_ny = datetime.now(ZoneInfo("America/New_York"))

data_atual = agora_ny.strftime("%Y-%m-%d")

print(
    "Horário de New York:",
    agora_ny.strftime("%Y-%m-%d %H:%M:%S %Z")
)


# =========================
# FUNÇÃO PARA OBTER DADOS
# =========================

def obter_previous(contrato):

    url = f"https://www.barchart.com/futures/quotes/{contrato}"

    print(f"Buscando {contrato}...")

    r = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    print(f"Status {contrato}: {r.status_code}")

    inicio = r.text.find(f'{{"{contrato}"')
    fim = r.text.find("</script>", inicio)

    if inicio == -1 or fim == -1:

        print(f"Não foi possível encontrar os dados de {contrato}")

        return None

    try:

        texto_json = r.text[inicio:fim].strip()

        dados = json.loads(texto_json)

        quote = dados[contrato]["quote"]

        print(
            f"{contrato} encontrado - "
            f"Previous Close: {quote.get('previousClose')}"
        )

        return quote

    except Exception as erro:

        print(f"Erro ao processar {contrato}: {erro}")

        return None


# =========================
# CONTRATOS
# =========================

contratos = [
    "SBV26",

    "SBH27",
    "SBK27",
    "SBN27",
    "SBV27",

    "SBH28",
    "SBK28",
    "SBN28",
    "SBV28",

    "SBH29",
    "SBK29",
    "SBN29",
    "SBV29"
]


# =========================
# COLETA DOS DADOS
# =========================

resultado = []

print("\nIniciando coleta...\n")


for contrato in contratos:

    dados = obter_previous(contrato)

    if dados is not None:

        resultado.append({
            "Data": data_atual,
            "Contrato": contrato,
            "Previous Close": dados.get("previousClose"),
            "Previous Open": dados.get("previousOpen"),
            "Previous High": dados.get("previousHigh"),
            "Previous Low": dados.get("previousLow"),
            "Weekly Previous Close": dados.get("weeklyPreviousClose"),
            "Weekly Previous High": dados.get("weeklyPreviousHigh"),
            "Weekly Previous Low": dados.get("weeklyPreviousLow"),
            "Monthly Previous Close": dados.get("monthlyPreviousClose"),
            "Monthly Previous High": dados.get("monthlyPreviousHigh"),
            "Monthly Previous Low": dados.get("monthlyPreviousLow"),
            "Trade Time": dados.get("tradeTime")
        })


# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(resultado)


# =========================
# RESULTADO
# =========================

print("\n==============================")
print("DATAFRAME PARA O EXCEL")
print("==============================\n")

print(df.to_string(index=False))


# =========================
# EXPORTAR PARA CSV
# =========================

df.to_csv("sugar_prices.csv", index=False)

print("\nArquivo sugar_prices.csv criado com sucesso.")

print("\n==============================")
print("Processo concluído.")
print("==============================")
