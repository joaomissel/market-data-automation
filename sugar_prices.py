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
    "SBV27"
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
            "Contrato": contrato,
            **dados
        })


# =========================
# DATAFRAME
# =========================

df = pd.DataFrame(resultado)


print("\n==============================")
print("RESULTADO FINAL")
print("==============================\n")

print(df)


# =========================
# FINALIZAÇÃO
# =========================

print("\n==============================")
print("Processo concluído.")
print("==============================")
