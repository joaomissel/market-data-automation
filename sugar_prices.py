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

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=15
        )

    except requests.RequestException as erro:

        print(
            f"Erro de conexão ao buscar {contrato}: {erro}"
        )

        return None

    print(f"Status {contrato}: {r.status_code}")

    # =========================
    # CONTRATO NÃO DISPONÍVEL
    # =========================

    if r.status_code == 404:

        print(
            f"{contrato} não está disponível no Barchart."
        )

        return None

    # =========================
    # ERRO DO SERVIDOR
    # =========================

    if r.status_code >= 500:

        print(
            f"Erro do servidor Barchart para {contrato}: "
            f"{r.status_code}"
        )

        return None

    # =========================
    # OUTROS STATUS HTTP
    # =========================

    if r.status_code != 200:

        print(
            f"Status inesperado para {contrato}: "
            f"{r.status_code}"
        )

        return None

    # =========================
    # LOCALIZAR JSON
    # =========================

    inicio = r.text.find(f'{{"{contrato}"')
    fim = r.text.find("</script>", inicio)

    if inicio == -1 or fim == -1:

        print(
            f"Não foi possível encontrar os dados de "
            f"{contrato}"
        )

        return None

    # =========================
    # PROCESSAR JSON
    # =========================

    try:

        texto_json = r.text[inicio:fim].strip()

        dados = json.loads(texto_json)

        quote = dados[contrato]["quote"]

        print(
            f"{contrato} encontrado - "
            f"Previous Close: "
            f"{quote.get('previousClose')}"
        )

        return quote

    except Exception as erro:

        print(
            f"Erro ao processar {contrato}: {erro}"
        )

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
    "SBV29",

    "SBH30",
    "SBK30",
    "SBN30",
    "SBV30",

    "SBH31",
    "SBK31",
    "SBN31",
    "SBV31"

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

            "Previous Close":
                dados.get("previousClose"),

            "Previous Open":
                dados.get("previousOpen"),

            "Previous High":
                dados.get("previousHigh"),

            "Previous Low":
                dados.get("previousLow"),

            "Weekly Previous Close":
                dados.get("weeklyPreviousClose"),

            "Weekly Previous High":
                dados.get("weeklyPreviousHigh"),

            "Weekly Previous Low":
                dados.get("weeklyPreviousLow"),

            "Monthly Previous Close":
                dados.get("monthlyPreviousClose"),

            "Monthly Previous High":
                dados.get("monthlyPreviousHigh"),

            "Monthly Previous Low":
                dados.get("monthlyPreviousLow"),

            "Trade Time":
                dados.get("tradeTime")

        })


# =========================
# VALIDAÇÃO DA COLETA
# =========================

print("\n==============================")
print("VALIDAÇÃO DA COLETA")
print("==============================")

print(
    f"\nContratos configurados: "
    f"{len(contratos)}"
)

print(
    f"Contratos coletados: "
    f"{len(resultado)}"
)


if len(resultado) == 0:

    print(
        "\nERRO: nenhum contrato foi coletado."
    )

    print(
        "Possível indisponibilidade do "
        "Barchart ou falha no GET."
    )

    raise RuntimeError(
        "Nenhum contrato foi coletado. "
        "Possível indisponibilidade do Barchart "
        "ou falha no GET."
    )


print(
    "\nColeta válida. "
    "Pelo menos um contrato foi encontrado."
)


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

print(
    df.to_string(index=False)
)


# =========================
# HISTÓRICO
# =========================

arquivo_historico = "sugar_history.csv"


try:

    historico = pd.read_csv(
        arquivo_historico
    )

    historico = pd.concat(
        [historico, df],
        ignore_index=True
    )

except (
    FileNotFoundError,
    pd.errors.EmptyDataError
):

    historico = df.copy()


# =========================
# REMOVER DUPLICIDADES
# =========================

historico = historico.drop_duplicates(
    subset=["Data", "Contrato"],
    keep="last"
)


# =========================
# ORDENAR HISTÓRICO
# =========================

historico = historico.sort_values(
    by=["Data", "Contrato"]
)


# =========================
# SALVAR HISTÓRICO
# =========================

historico.to_csv(
    arquivo_historico,
    index=False
)

print(
    "\nHistórico atualizado com sucesso."
)


# =========================
# EXPORTAR COTAÇÃO ATUAL
# =========================

df.to_csv(
    "sugar_prices.csv",
    index=False
)

print(
    "\nArquivo sugar_prices.csv "
    "criado com sucesso."
)


# =========================
# FINAL
# =========================

print("\n==============================")
print("Processo concluído.")
print("==============================")
